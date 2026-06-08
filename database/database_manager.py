import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.db_path = ("database/seds.db")

        self.create_tables()

    def get_connection(self):

        return sqlite3.connect(self.db_path)

    def create_tables(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            object_class TEXT NOT NULL,

            confidence REAL NOT NULL,

            image_path TEXT
        )
        """)

        conn.commit()

        conn.close()
