-- ==========================================
-- Freim: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS developers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS statuses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    priority TEXT NOT NULL,
    status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    developer_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES statuses (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (developer_id) REFERENCES developers (id)
);

