import heapq
import hashlib
import os
import sys

# Ensure production paths
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from storage.db import db

class TaskScheduler:
    """
    Zero-Waste Priority Scheduler.
    Handles deduplication via hashing and priority-based execution.
    """
    def __init__(self):
        self.queue = [] # Priority queue (min-heap, so we use -priority)
        self.seen_hashes = set()
        self._load_pending_tasks()

    def _load_pending_tasks(self):
        rows = db.query("SELECT task_hash, task_name, priority FROM tasks WHERE status = 'pending'")
        for h, name, p in rows:
            self.seen_hashes.add(h)
            heapq.heappush(self.queue, (-p, {"hash": h, "name": name}))

    def add_task(self, name, priority=1, data=None):
        task_str = f"{name}_{str(data)}"
        task_hash = hashlib.md5(task_str.encode()).hexdigest()

        if task_hash in self.seen_hashes:
            return False # Zero-waste: don't repeat work

        # Persist to DB
        db.execute(
            "INSERT OR IGNORE INTO tasks (task_hash, task_name, priority) VALUES (?, ?, ?)",
            (task_hash, name, priority)
        )
        
        self.seen_hashes.add(task_hash)
        heapq.heappush(self.queue, (-priority, {"hash": task_hash, "name": name, "data": data}))
        return True

    def get_next_task(self):
        if not self.queue:
            return None
        _, task = heapq.heappop(self.queue)
        # Mark as processing in DB
        db.execute("UPDATE tasks SET status = 'processing' WHERE task_hash = ?", (task["hash"],))
        return task

    def complete_task(self, task_hash):
        db.execute("UPDATE tasks SET status = 'completed' WHERE task_hash = ?", (task_hash,))

scheduler = TaskScheduler()
