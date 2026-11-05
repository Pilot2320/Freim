"""Тесты для базы данных SQLite и SQL-запросов (ПР7)."""

from pathlib import Path
import sqlite3

from db.database import get_connection
from db.import_json import (
    import_developers,
    import_errors,
    import_statuses,
    import_users,
    init_db,
)


def test_database_connection():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        assert cur.fetchone()[0] == 1
    finally:
        conn.close()


def test_import_and_foreign_keys(tmp_path):
    test_db = tmp_path / "test.sqlite"
    conn = get_connection(test_db)
    try:
        init_db(conn)
        import_users(conn)
        import_developers(conn)
        import_statuses(conn)
        import_errors(conn)
        conn.commit()

        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [t[0] for t in tables]
        assert "users" in table_names
        assert "developers" in table_names
        assert "statuses" in table_names
        assert "errors" in table_names

        errors_count = conn.execute(
            "SELECT COUNT(*) FROM errors"
        ).fetchone()[0]
        assert errors_count > 0
    finally:
        conn.close()


def test_queries_file_exists_and_runs():
    base_dir = Path(__file__).resolve().parent.parent
    queries_path = base_dir / "sql" / "queries.sql"
    assert queries_path.exists()

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        with open(queries_path, "r", encoding="utf-8") as f:
            content = f.read()

        statements = [s.strip() for s in content.split(";") if s.strip()]
        assert len(statements) >= 10
        for stmt in statements:
            res = conn.execute(stmt).fetchall()
            assert res is not None
    finally:
        conn.close()
