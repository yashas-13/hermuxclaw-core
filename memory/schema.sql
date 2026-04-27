-- memory/schema.sql
-- Persistent storage for Skill definitions and Evolution history

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
