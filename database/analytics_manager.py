from database.database_manager import (
    DatabaseManager
)


class AnalyticsManager:

    def __init__(self):

        self.db = DatabaseManager()

    def total_detections(self):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM detections
            """
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    def average_confidence(self):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT AVG(confidence)
            FROM detections
            """
        )

        avg = cursor.fetchone()[0]

        conn.close()

        return avg
        
    def get_all_detections(self):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM detections
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows
