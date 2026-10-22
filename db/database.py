"""Модуль подключения к базе данных SQLite."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "freim.sqlite"


def get_connection(db_path=None) -> sqlite3.Connection:
    """Создать и настроить подключение к SQLite с внешними ключами."""
    target_path = Path(db_path) if db_path else DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
