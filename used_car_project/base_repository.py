# base_repository.py
import sqlite3

class BaseRepository:
    def __init__(self, db_path='used_car.db'):
        self.db_path = db_path

    def get_connection(self):
        """Establish a new database connection."""
        return sqlite3.connect(self.db_path)

    def fetch_all(self, query, params=()):
        """Fetch all rows for a given query."""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Enables column access by name
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def fetch_one(self, query, params=()):
        """Fetch a single row for a given query."""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    def execute_query(self, query, params=()):
        """Execute an INSERT, UPDATE, or DELETE query."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
