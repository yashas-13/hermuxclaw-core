import os
import sys

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from storage.db import db

class GraphStore:
    """
    Hybrid Graph Storage.
    Persistent in SQLite, Adjacency logic in memory.
    """
    def __init__(self):
        self.call_graph = {}
        self.dep_graph = {}
        self._load_from_db()

    def _load_from_db(self):
        # Load calls
        rows = db.query("SELECT caller, callee FROM calls")
        for caller, callee in rows:
            self.call_graph.setdefault(caller, []).append(callee)
        
        # Load dependencies
        rows = db.query("SELECT file, depends_on FROM dependencies")
        for f, d in rows:
            self.dep_graph.setdefault(f, []).append(d)

    def add_call(self, caller, callee, is_runtime=False):
        self.call_graph.setdefault(caller, []).append(callee)
        db.execute(
            "INSERT INTO calls (caller, callee, is_runtime) VALUES (?, ?, ?)",
            (caller, callee, 1 if is_runtime else 0)
        )

    def add_dependency(self, file, dep):
        self.dep_graph.setdefault(file, []).append(dep)
        db.execute(
            "INSERT INTO dependencies (file, depends_on) VALUES (?, ?)",
            (file, dep)
        )

graph_store = GraphStore()
