# memory/skill_registry.py
import sqlite3, json, time, os

# Default database path
DB_PATH = os.path.expanduser(os.getenv("HX_DB_PATH", "~/hermuxclaw/memory/registry.db"))

class SkillRegistry:
    """
    SQLite-backed skill registry — the persistent memory of HermuXclaw.
    Tracks skill metadata, scores, and historical usage.
    """
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        # We also read from our schema.sql if needed, but here we embed it for robustness
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                version TEXT,
                file_path TEXT,
                score REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                last_used REAL,
                status TEXT DEFAULT 'active',
                meta_json TEXT,
                created_at REAL DEFAULT (strftime('%s', 'now'))
            );
            CREATE TABLE IF NOT EXISTS evolution_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT,
                f1_score REAL,
                latency_ms REAL,
                passed INTEGER,
                timestamp REAL DEFAULT (strftime('%s', 'now'))
            );
        """)
        self.conn.commit()

    def register(self, skill_info: dict):
        """Register or update a skill's metadata and score."""
        self.conn.execute("""
            INSERT OR REPLACE INTO skills
            (id, name, version, file_path, score, meta_json)
            VALUES (?,?,?,?,?,?)
        """, (skill_info.get("id", skill_info["name"]),
              skill_info["name"], skill_info.get("version","1.0.0"),
              skill_info.get("file_path",""),
              skill_info.get("latency_ms", 0),
              json.dumps(skill_info)))
        self.conn.commit()

    def record_usage(self, name: str, success: bool):
        """Update usage stats for a specific skill."""
        self.conn.execute("""
            UPDATE skills SET usage_count = usage_count + 1,
            last_used = ? WHERE name = ?
        """, (time.time(), name))
        self.conn.commit()

    def get_all(self):
        """Retrieve all active skills from the registry."""
        cur = self.conn.execute(
            "SELECT name, version, score, usage_count, status FROM skills")
        return [dict(zip([d[0] for d in cur.description], row))
                for row in cur.fetchall()]

    def close(self):
        self.conn.close()
