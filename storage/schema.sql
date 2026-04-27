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
    classification TEXT, -- Semantic Tagging
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY,
    name TEXT,
    version TEXT DEFAULT '1.0.0',
    content TEXT,
    hash TEXT UNIQUE,
    fitness_score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'candidate', -- candidate, verified, deprecated
    parents TEXT, -- JSON list of parent skill IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evolution_runs (
    id INTEGER PRIMARY KEY,
    skill_id INTEGER,
    intent TEXT,
    benchmark_ms INTEGER,
    status TEXT,
    log TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(skill_id) REFERENCES skills(id)
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

CREATE TABLE IF NOT EXISTS workflow_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    directive TEXT,
    status TEXT,
    iq_score REAL, -- Aggregate of the 18 outcomes
    latency_total_ms INTEGER,
    energy_consumed INTEGER,
    skills_created INTEGER DEFAULT 0,
    knowledge_points INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


