"""Представление главной страницы с выборкой показателей из SQLite."""

import sqlite3

from django.shortcuts import render

from db.database import get_connection


def _load_error_context() -> dict:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        total = conn.execute("SELECT COUNT(*) FROM errors").fetchone()[0]
        open_errors = conn.execute(
            "SELECT COUNT(*) FROM errors WHERE status_id != 4"
        ).fetchone()[0]
        high_pri = conn.execute(
            "SELECT COUNT(*) FROM errors WHERE priority = 'Высокий'"
        ).fetchone()[0]
        recent = conn.execute(
            """
            SELECT
                errors.id,
                errors.title,
                errors.severity,
                errors.priority,
                statuses.name AS status,
                statuses.name AS status_name
            FROM errors
            JOIN statuses ON errors.status_id = statuses.id
            ORDER BY errors.id DESC
            LIMIT 5
            """
        ).fetchall()
        return {
            "errors": recent,
            "total_errors": total,
            "open_errors": open_errors,
            "high_priority": high_pri,
        }
    finally:
        conn.close()


def home(request):
    """Главная страница сервиса."""
    context = _load_error_context()
    return render(request, "homepage/index.html", context)


def index(request):
    """Алиас представления главной страницы."""
    return home(request)
