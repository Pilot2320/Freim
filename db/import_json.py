"""Скрипт переноса данных из JSON-файлов в таблицы SQLite."""

import json
from pathlib import Path
import sqlite3

from db.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"
DEVELOPERS_FILE = BASE_DIR / "data" / "developers.json"
STATUSES_FILE = BASE_DIR / "data" / "statuses.json"
ERRORS_FILE = BASE_DIR / "data" / "errors.json"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def load_json(filename: Path):
    """Прочитать данные из JSON-файла."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def init_db(conn: sqlite3.Connection) -> None:
    """Создать структуру таблиц по схеме sql/schema.sql."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        conn.executescript(file.read())


def import_users(conn: sqlite3.Connection) -> None:
    """Импортировать пользователей."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [(u["id"], u["name"], u["email"]) for u in users],
    )


def import_developers(conn: sqlite3.Connection) -> None:
    """Импортировать разработчиков."""
    developers = load_json(DEVELOPERS_FILE)
    conn.executemany(
        """
        INSERT INTO developers (id, name, specialization)
        VALUES (?, ?, ?)
        """,
        [(d["id"], d["name"], d["specialization"]) for d in developers],
    )


def import_statuses(conn: sqlite3.Connection) -> None:
    """Импортировать статусы."""
    statuses = load_json(STATUSES_FILE)
    conn.executemany(
        """
        INSERT INTO statuses (id, name)
        VALUES (?, ?)
        """,
        [(s["id"], s["name"]) for s in statuses],
    )


def import_errors(conn: sqlite3.Connection) -> None:
    """Импортировать ошибки со связями."""
    errors = load_json(ERRORS_FILE)
    status_rows = conn.execute("SELECT id, name FROM statuses").fetchall()
    status_map = {name: sid for sid, name in status_rows}

    records = []
    for err in errors:
        raw_status = err["status"]
        if isinstance(raw_status, int):
            status_id = raw_status
        elif raw_status in status_map:
            status_id = status_map[raw_status]
        else:
            status_id = int(raw_status) if str(raw_status).isdigit() else 1

        records.append(
            (
                err["id"],
                err["title"],
                err["description"],
                err["severity"],
                err["priority"],
                status_id,
                err["user_id"],
                err["developer_id"],
            )
        )

    conn.executemany(
        """
        INSERT INTO errors (
            id, title, description, severity, priority,
            status_id, user_id, developer_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records,
    )


def main() -> None:
    """Основная функция импорта."""
    conn = get_connection()
    try:
        init_db(conn)
        conn.execute("DELETE FROM errors")
        conn.execute("DELETE FROM statuses")
        conn.execute("DELETE FROM developers")
        conn.execute("DELETE FROM users")

        import_users(conn)
        import_developers(conn)
        import_statuses(conn)
        import_errors(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
