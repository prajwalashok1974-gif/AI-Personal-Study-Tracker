PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS study_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT,
    start_time TEXT,
    end_time TEXT,
    duration_min INTEGER,
    subject TEXT,
    technique TEXT,
    distractions INTEGER,
    mood INTEGER,
    caffeine_mg INTEGER,
    productivity INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT);
