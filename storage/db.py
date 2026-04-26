import sqlite3
import os

class DB:
    def __init__(self):
        self.db_path = os.path.expanduser("~/hermuxclaw/storage/hx.db")
        self.schema_path = os.path.expanduser("~/hermuxclaw/storage/schema.sql")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        with open(self.schema_path, "r") as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()

db = DB() # Global instance
