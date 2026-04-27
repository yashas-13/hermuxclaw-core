# storage/local_store.py
import sqlite3
import os
from typing import List, Dict, Any

class LocalStore:
    """
    SQLite abstraction wrapper.
    Used for structured access to the skill registry and evolution logs.
    """
    def __init__(self, db_path: str):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def execute(self, query: str, params: tuple = ()) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, params)
            conn.commit()

    def query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(query, params)
            return [dict(row) for row in cur.fetchall()]
