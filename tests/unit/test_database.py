"""Isolated tests for the versioned SQLite database manager."""

from contextlib import contextmanager
import sqlite3

import pytest

from database.database_manager import (
    DatabaseManager,
    DatabaseMigrationError,
    SCHEMA_VERSION,
)


TARGET_SCHEMA = [
    ("id", "INTEGER", 0, None, 1),
    ("timestamp", "TEXT", 1, None, 0),
    ("object_class", "TEXT", 1, None, 0),
    ("confidence", "REAL", 1, None, 0),
    ("image_path", "TEXT", 0, None, 0),
    ("event_id", "TEXT", 0, None, 0),
]


@contextmanager
def _sqlite_connection(path):
    """Open a test connection with explicit commit, rollback, and close."""
    conn = sqlite3.connect(path)
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def _schema(path):
    with _sqlite_connection(path) as conn:
        return [
            (row[1], row[2].upper(), row[3], row[4], row[5])
            for row in conn.execute("PRAGMA table_info(detections)")
        ]


def _user_version(path):
    with _sqlite_connection(path) as conn:
        return conn.execute("PRAGMA user_version").fetchone()[0]


def _create_legacy_database(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with _sqlite_connection(path) as conn:
        conn.execute(
            """
            CREATE TABLE detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                object_class TEXT NOT NULL,
                confidence REAL NOT NULL,
                image_path TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO detections
                (timestamp, object_class, confidence, image_path)
            VALUES (?, ?, ?, ?)
            """,
            ("2026-01-02 03:04:05", "elephant", 0.91, "sample.jpg"),
        )


def _create_unversioned_six_column_database(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with _sqlite_connection(path) as conn:
        conn.execute(
            """
            CREATE TABLE detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                object_class TEXT NOT NULL,
                confidence REAL NOT NULL,
                image_path TEXT,
                event_id TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO detections
                (timestamp, object_class, confidence, image_path, event_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("2026-01-02", "elephant", 0.88, "old.jpg", "EVT-existing"),
        )


class _ConnectionSpy:
    def __init__(self, connection, fail_on_insert=False):
        self.connection = connection
        self.fail_on_insert = fail_on_insert
        self.closed = False
        self.rollback_count = 0
        self.in_transaction_on_close = None

    @property
    def in_transaction(self):
        return self.connection.in_transaction

    def execute(self, sql, parameters=()):
        if self.fail_on_insert and sql.lstrip().upper().startswith("INSERT"):
            raise sqlite3.OperationalError("injected insert failure")
        return self.connection.execute(sql, parameters)

    def rollback(self):
        self.rollback_count += 1
        return self.connection.rollback()

    def close(self):
        self.in_transaction_on_close = self.connection.in_transaction
        self.closed = True
        return self.connection.close()

    def __getattr__(self, name):
        return getattr(self.connection, name)


def test_fresh_database_initialization_creates_version_one_schema(tmp_path):
    path = tmp_path / "nested" / "seds.db"

    DatabaseManager(path)

    assert path.is_file()
    assert _schema(path) == TARGET_SCHEMA
    assert _user_version(path) == SCHEMA_VERSION


def test_insert_and_retrieve_detection_with_event_id(tmp_path):
    manager = DatabaseManager(tmp_path / "seds.db")

    manager.insert_detection(
        timestamp="2026-02-03 04:05:06",
        object_class="elephant",
        confidence=0.94,
        image_path="sample.jpg",
        event_id="EVT-12345678",
    )

    rows = manager.get_all_detections()
    assert len(rows) == 1
    assert rows[0][1:] == (
        "2026-02-03 04:05:06",
        "elephant",
        0.94,
        "sample.jpg",
        "EVT-12345678",
    )


def test_legacy_five_column_database_migrates_and_preserves_rows(tmp_path):
    path = tmp_path / "legacy" / "seds.db"
    _create_legacy_database(path)

    manager = DatabaseManager(path)

    assert _schema(path) == TARGET_SCHEMA
    assert _user_version(path) == SCHEMA_VERSION
    assert manager.get_all_detections() == [
        (1, "2026-01-02 03:04:05", "elephant", 0.91, "sample.jpg", None)
    ]


def test_unversioned_six_column_database_is_adopted_without_rewriting_rows(
    tmp_path,
):
    path = tmp_path / "already-upgraded.db"
    _create_unversioned_six_column_database(path)
    with _sqlite_connection(path) as conn:
        before = conn.execute("SELECT * FROM detections").fetchall()

    manager = DatabaseManager(path)

    assert _schema(path) == TARGET_SCHEMA
    assert _user_version(path) == SCHEMA_VERSION
    assert manager.get_all_detections() == before


def test_repeated_migration_is_idempotent(tmp_path):
    path = tmp_path / "seds.db"
    manager = DatabaseManager(path)
    manager.insert_detection("2026-01-01", "elephant", 0.8, "x.jpg", "EVT-one")
    before = manager.get_all_detections()

    manager.migrate()
    manager.migrate()

    assert _schema(path) == TARGET_SCHEMA
    assert _user_version(path) == SCHEMA_VERSION
    assert manager.get_all_detections() == before


def test_unknown_schema_is_rejected_without_data_loss(tmp_path):
    path = tmp_path / "unknown.db"
    with _sqlite_connection(path) as conn:
        conn.execute("CREATE TABLE detections (id TEXT, payload BLOB)")
        conn.execute("INSERT INTO detections VALUES ('legacy', X'01')")

    with pytest.raises(DatabaseMigrationError, match="Unrecognized detections"):
        DatabaseManager(path)

    with _sqlite_connection(path) as conn:
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 0
        assert conn.execute("SELECT id, payload FROM detections").fetchall() == [
            ("legacy", b"\x01")
        ]


def test_database_with_other_tables_is_not_treated_as_fresh(tmp_path):
    path = tmp_path / "other-table.db"
    with _sqlite_connection(path) as conn:
        conn.execute("CREATE TABLE unrelated (payload TEXT)")
        conn.execute("INSERT INTO unrelated VALUES ('keep')")

    with pytest.raises(DatabaseMigrationError, match="refusing fresh initialization"):
        DatabaseManager(path)

    with _sqlite_connection(path) as conn:
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 0
        assert conn.execute("SELECT payload FROM unrelated").fetchall() == [
            ("keep",)
        ]
        assert conn.execute(
            "SELECT name FROM sqlite_master WHERE name = 'detections'"
        ).fetchone() is None


def test_unsupported_future_schema_version_is_rejected(tmp_path):
    path = tmp_path / "future.db"
    DatabaseManager(path)
    with _sqlite_connection(path) as conn:
        conn.execute("PRAGMA user_version = 2")

    with pytest.raises(DatabaseMigrationError, match="newer than the supported"):
        DatabaseManager(path)

    assert _user_version(path) == 2
    assert _schema(path) == TARGET_SCHEMA


def test_failed_migration_rolls_back_schema_and_version(tmp_path, monkeypatch):
    path = tmp_path / "legacy.db"
    _create_legacy_database(path)
    manager = DatabaseManager.__new__(DatabaseManager)
    manager.db_path = str(path)
    manager._db_path = path

    def fail_version_update(conn, version):
        raise RuntimeError("injected migration failure")

    monkeypatch.setattr(
        manager, "_set_user_version", fail_version_update
    )
    with pytest.raises(RuntimeError, match="injected migration failure"):
        manager.migrate()

    assert _schema(path) == TARGET_SCHEMA[:-1]
    assert _user_version(path) == 0
    with _sqlite_connection(path) as conn:
        assert conn.execute("SELECT * FROM detections").fetchall() == [
            (1, "2026-01-02 03:04:05", "elephant", 0.91, "sample.jpg")
        ]


def test_insert_closes_connection_after_success(tmp_path, monkeypatch):
    manager = DatabaseManager(tmp_path / "seds.db")
    spy = _ConnectionSpy(sqlite3.connect(manager.db_path))
    monkeypatch.setattr(manager, "get_connection", lambda: spy)

    manager.insert_detection("2026-03-04", "elephant", 0.95, "x.jpg", "EVT-ok")

    assert spy.closed
    assert spy.in_transaction_on_close is False


def test_failed_insert_rolls_back_and_closes_connection(tmp_path, monkeypatch):
    manager = DatabaseManager(tmp_path / "seds.db")
    spy = _ConnectionSpy(
        sqlite3.connect(manager.db_path), fail_on_insert=True
    )
    monkeypatch.setattr(manager, "get_connection", lambda: spy)

    with pytest.raises(sqlite3.OperationalError, match="injected insert failure"):
        manager.insert_detection("2026-03-04", "elephant", 0.95, "x.jpg", "EVT-no")

    assert spy.closed
    assert spy.rollback_count == 1
    assert spy.in_transaction_on_close is False


def test_connection_context_closes_after_success_and_failure(tmp_path, monkeypatch):
    manager = DatabaseManager(tmp_path / "seds.db")
    successful = _ConnectionSpy(sqlite3.connect(manager.db_path))
    monkeypatch.setattr(manager, "get_connection", lambda: successful)

    with manager.connection() as conn:
        conn.execute("SELECT COUNT(*) FROM detections").fetchone()

    assert successful.closed

    failed = _ConnectionSpy(sqlite3.connect(manager.db_path))
    monkeypatch.setattr(manager, "get_connection", lambda: failed)
    with pytest.raises(sqlite3.OperationalError, match="no such table"):
        with manager.connection() as conn:
            conn.execute("SELECT * FROM missing_table")

    assert failed.closed


def test_migration_closes_connection_after_success_and_failure(tmp_path, monkeypatch):
    valid_path = tmp_path / "valid.db"
    valid_manager = DatabaseManager(valid_path)
    successful = _ConnectionSpy(sqlite3.connect(valid_path))
    monkeypatch.setattr(valid_manager, "get_connection", lambda: successful)

    valid_manager.migrate()

    assert successful.closed
    assert successful.in_transaction_on_close is False

    invalid_path = tmp_path / "invalid.db"
    with _sqlite_connection(invalid_path) as conn:
        conn.execute("CREATE TABLE detections (id TEXT)")
    invalid_manager = DatabaseManager.__new__(DatabaseManager)
    invalid_manager.db_path = str(invalid_path)
    invalid_manager._db_path = invalid_path
    failed = _ConnectionSpy(sqlite3.connect(invalid_path))
    monkeypatch.setattr(invalid_manager, "get_connection", lambda: failed)

    with pytest.raises(DatabaseMigrationError):
        invalid_manager.migrate()

    assert failed.closed
    assert failed.rollback_count == 1
    assert failed.in_transaction_on_close is False
