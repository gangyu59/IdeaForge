CREATE TABLE IF NOT EXISTS idea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS discussion_round (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER,
    round INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_output (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER,
    round INTEGER,
    agent_name TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS idea_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_idea_id INTEGER NOT NULL,
    child_idea_id INTEGER NOT NULL,
    source_round TEXT,           -- 例如 '3' 或 'final'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- db/schema.sql 中追加（已存在 schema 不改）

CREATE TABLE IF NOT EXISTS idea_section (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER NOT NULL,
    section_key TEXT NOT NULL,        -- product_overview / users_and_scenarios / ...
    content TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'undefined',  -- undefined | unstable | stable
    updated_at TEXT NOT NULL,
    UNIQUE (idea_id, section_key)
);
