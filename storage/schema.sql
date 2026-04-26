-- HERMUXCLAW PRODUCTION SCHEMA
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    hash TEXT,
    last_scanned TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS functions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    file_id INTEGER,
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY,
    caller TEXT,
    callee TEXT,
    is_runtime BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS dependencies (
    id INTEGER PRIMARY KEY,
    file TEXT,
    depends_on TEXT
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    task_hash TEXT UNIQUE,
    task_name TEXT,
    priority INTEGER,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS energy_stats (
    id INTEGER PRIMARY KEY,
    current_energy INTEGER,
    last_regenerated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
