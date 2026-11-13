"""SQLite connection and schema management for SEDS V2."""

from contextlib import contextmanager
from pathlib import Path
import re
import sqlite3
from typing import Iterator


SCHEMA_VERSION = 1

_DETECTIONS_COLUMNS = (
    ("id", "INTEGER", 0, None, 1),
    ("timestamp", "TEXT", 1, None, 0),
    ("object_class", "TEXT", 1, None, 0),
    ("confidence", "REAL", 1, None, 0),
    ("image_path", "TEXT", 0, None, 0),
    ("event_id", "TEXT", 0, None, 0),
)
_LEGACY_DETECTIONS_COLUMNS = _DETECTIONS_COLUMNS[:-1]
_DETECTIONS_TABLE_SQL = """
CREATE TABLE detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    object_class TEXT NOT NULL,
    confidence REAL NOT NULL,
    image_path TEXT,
    event_id TEXT
)
"""


class DatabaseMigrationError(RuntimeError):
    """Raised when a database schema cannot be safely migrated or adopted."""


class DatabaseManager:
    """Manage SEDS SQLite initialization, schema migration, and queries.

    Args:
        db_path: SQLite file path. Defaults to ``database/seds.db`` relative
            to the current working directory.
    """

    def __init__(self, db_path: str | Path = "database/seds.db") -> None:
        # Keep the historical string attribute while accepting Path inputs.
        self.db_path = str(db_path)
        self._db_path = Path(db_path)
        self.initialize_database()

    def initialize_database(self) -> None:
        """Create the parent directory and migrate or validate the schema."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self.migrate()

    def get_connection(self) -> sqlite3.Connection:
        """Return a new SQLite connection to the configured database."""
        return sqlite3.connect(self.db_path)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a connection and close it regardless of query outcome."""
        conn = self.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def create_tables(self) -> None:
        """Backward-compatible initializer; schema changes use migrations."""
        self.initialize_database()

    def migrate(self) -> None:
        """Apply the supported schema migration atomically and idempotently."""
        conn = self.get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version > SCHEMA_VERSION:
                raise DatabaseMigrationError(
                    f"Database schema version {version} is newer than the "
                    f"supported version {SCHEMA_VERSION}."
                )

            table_exists = conn.execute(
                """
                SELECT 1
                FROM sqlite_master
                WHERE type = 'table' AND name = 'detections'
                """
            ).fetchone() is not None

            if not table_exists:
                if version != 0:
                    raise DatabaseMigrationError(
                        f"Database schema version is {version}, but the "
                        "detections table is missing."
                    )
                other_tables = conn.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                    """
                ).fetchall()
                if other_tables:
                    names = ", ".join(row[0] for row in other_tables)
                    raise DatabaseMigrationError(
                        "Database has no detections table but contains other "
                        f"tables ({names}); refusing fresh initialization."
                    )
                conn.execute(_DETECTIONS_TABLE_SQL)
                self._validate_detections_schema(conn, _DETECTIONS_COLUMNS)
                self._set_user_version(conn, SCHEMA_VERSION)
            elif version == 0:
                if self._has_expected_schema(conn, _LEGACY_DETECTIONS_COLUMNS):
                    conn.execute(
                        "ALTER TABLE detections ADD COLUMN event_id TEXT"
                    )
                    self._validate_detections_schema(conn, _DETECTIONS_COLUMNS)
                    self._set_user_version(conn, SCHEMA_VERSION)
                elif self._has_expected_schema(conn, _DETECTIONS_COLUMNS):
                    # Adopt a compatible six-column database created before
                    # user_version was introduced; do not rewrite its records.
                    self._set_user_version(conn, SCHEMA_VERSION)
                else:
                    raise DatabaseMigrationError(
                        "Unrecognized detections schema at user_version 0; "
                        "expected the legacy five-column or target "
                        "six-column schema. No changes were applied."
                    )
            else:
                self._validate_detections_schema(conn, _DETECTIONS_COLUMNS)

            conn.commit()
        except BaseException:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _set_user_version(conn: sqlite3.Connection, version: int) -> None:
        """Set SQLite's application schema version within the current txn."""
        conn.execute(f"PRAGMA user_version = {int(version)}")

    @classmethod
    def _has_expected_schema(
        cls,
        conn: sqlite3.Connection,
        expected_columns: tuple[tuple[str, str, int, str | None, int], ...],
    ) -> bool:
        try:
            cls._validate_detections_schema(conn, expected_columns)
        except DatabaseMigrationError:
            return False
        return True

    @staticmethod
    def _validate_detections_schema(
        conn: sqlite3.Connection,
        expected_columns: tuple[tuple[str, str, int, str | None, int], ...],
    ) -> None:
        """Validate column order, affinity, nullability, defaults and keys."""
        info = conn.execute("PRAGMA table_info(detections)").fetchall()
        actual_columns = tuple(
            (row[1], row[2].upper(), row[3], row[4], row[5]) for row in info
        )
        if actual_columns != expected_columns:
            raise DatabaseMigrationError(
                "Unrecognized detections columns or constraints: "
                f"found {actual_columns!r}, expected {expected_columns!r}."
            )

        table_row = conn.execute(
            "SELECT sql FROM sqlite_master "
            "WHERE type = 'table' AND name = 'detections'"
        ).fetchone()
        table_sql = table_row[0] if table_row else ""
        if not re.search(r"\bAUTOINCREMENT\b", table_sql, re.IGNORECASE):
            raise DatabaseMigrationError(
                "Unrecognized detections constraint: id must use "
                "INTEGER PRIMARY KEY AUTOINCREMENT."
            )
        if re.search(
            r"\b(CHECK|UNIQUE|REFERENCES|COLLATE)\b", table_sql, re.IGNORECASE
        ):
            raise DatabaseMigrationError(
                "Unrecognized additional constraint in detections table; "
                "manual schema review is required."
            )
        if conn.execute("PRAGMA foreign_key_list(detections)").fetchall():
            raise DatabaseMigrationError(
                "Unrecognized foreign key constraint on detections."
            )
        indexes = conn.execute("PRAGMA index_list(detections)").fetchall()
        if any(row[2] for row in indexes):
            raise DatabaseMigrationError(
                "Unrecognized unique constraint on detections."
            )

    def insert_detection(
        self,
        timestamp: str,
        object_class: str,
        confidence: float,
        image_path: str,
        event_id: str,
    ) -> None:
        """Insert one detection in a transaction and close the connection."""
        conn = self.get_connection()
        try:
            conn.execute("BEGIN")
            conn.execute(
                """
                INSERT INTO detections
                    (timestamp, object_class, confidence, image_path, event_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, object_class, confidence, image_path, event_id),
            )
            conn.commit()
        except BaseException:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_detections(self) -> list[tuple]:
        """Return detection tuples in the established six-column order."""
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT id, timestamp, object_class, confidence, image_path,
                       event_id
                FROM detections
                """
            ).fetchall()
        return rows
