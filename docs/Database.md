# Database

## SQLite location and initialization

`DatabaseManager` creates the `database/` directory if needed and uses the working-directory-relative path `database/seds.db`. Its constructor calls `create_tables()`, which runs `CREATE TABLE IF NOT EXISTS`. The dashboard's `AnalyticsManager` constructs a `DatabaseManager`, so opening a dashboard page also invokes that initialization path.

Run commands from the repository root to keep the relative path stable. The database file is ignored by Git and local contents are not distributed with a clone.

## Source-defined schema

The checked-in `DatabaseManager.create_tables()` defines:

| Column | SQLite definition | Meaning |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Local row identifier. |
| `timestamp` | `TEXT NOT NULL` | Detection timestamp string. |
| `object_class` | `TEXT NOT NULL` | Model class label. |
| `confidence` | `REAL NOT NULL` | Model confidence value. |
| `image_path` | `TEXT` | Optional image path string. |

### Known `event_id` mismatch

`insert_detection()` names and supplies a sixth column, `event_id`, but `create_tables()` does not define that column. On a fresh database, an insert is expected to fail with a missing-column SQLite error. `dashboard/pages/History.py` also labels six selected row values, so its expected shape includes `event_id`. A local ignored database may have a different schema and can conceal this defect.

No schema change is made by this documentation. A code correction should establish how existing databases are migrated and preserved before it is implemented.

## DatabaseManager behavior

- `get_connection()` returns a standard `sqlite3` connection.
- `create_tables()` creates the five-column table if absent.
- `insert_detection(...)` inserts timestamp, class, confidence, image path, and event ID.
- `get_all_detections()` returns all rows with `SELECT *` and no explicit ordering.

Connections are closed after successful statements, but the code does not use context managers/finally blocks. An exception can leave cleanup incomplete. No foreign keys, indexes, validation constraints for confidence, or schema version table are defined.

## AnalyticsManager queries

The dashboard-facing manager executes direct SQL for:

```sql
SELECT COUNT(*) FROM detections;
SELECT AVG(confidence) FROM detections;
SELECT * FROM detections ORDER BY id DESC;
SELECT confidence FROM detections;
```

On an empty table, SQLite `AVG` returns `NULL`, exposed in Python as `None`. The home page currently calls `round(value, 2)`, which can fail for that empty-database result.

## Event ID relationship

`DetectionEvent.event_id` defaults to an empty string. `EventManager` can generate an `EVT-` ID, but it does not enforce assignment or maintain a separate event table. The current relationship is a plain intended column value, not a foreign key. Repeated rows can share an ID if the caller assigns the same value; no time/space aggregation is performed.

## Useful SQL

Inspect the table definition and row count:

```sql
PRAGMA table_info(detections);
SELECT COUNT(*) FROM detections;
SELECT id, timestamp, object_class, confidence, image_path FROM detections ORDER BY id DESC LIMIT 20;
```

These are read-only inspection examples. To check for an `event_id` column, inspect `PRAGMA table_info(detections)` before querying it.

## Backup and recovery

No project backup/restore command is implemented. Before maintenance, stop processes that may write to the database and make a filesystem copy of `database/seds.db` to a separate safe location. Verify a backup by opening the copy with SQLite and running `PRAGMA integrity_check;`. Do not replace or delete an existing database as part of troubleshooting.

## Migration strategy

There is currently no migration framework or schema version tracking. Any future schema correction should:

1. Back up the database and retain all rows.
2. Inspect actual columns and database version before applying changes.
3. Apply a repeatable, versioned migration (including `event_id` handling and defaults for historical rows).
4. Verify row counts, constraints, and application queries after migration.
5. Keep a recovery path and document supported old/new schema versions.

This is a recommended strategy, not implemented migration behavior.
