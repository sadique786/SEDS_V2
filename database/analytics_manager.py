"""Read-only aggregate queries used by the dashboard."""

from database.database_manager import DatabaseManager


class AnalyticsManager:
    """Provide dashboard queries while preserving their return formats."""

    def __init__(self) -> None:
        self.db = DatabaseManager()

    def total_detections(self) -> int:
        with self.db.connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM detections").fetchone()
        return row[0]

    def average_confidence(self) -> float | None:
        with self.db.connection() as conn:
            row = conn.execute("SELECT AVG(confidence) FROM detections").fetchone()
        return row[0]

    def get_all_detections(self) -> list[tuple]:
        with self.db.connection() as conn:
            rows = conn.execute(
                """
                SELECT id, timestamp, object_class, confidence, image_path,
                       event_id
                FROM detections
                ORDER BY id DESC
                """
            ).fetchall()
        return rows

    def confidence_distribution(self) -> list[float]:
        with self.db.connection() as conn:
            rows = conn.execute(
                "SELECT confidence FROM detections"
            ).fetchall()
        return [row[0] for row in rows]
