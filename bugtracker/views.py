"""Представления для работы с ошибками через SQLite."""

import sqlite3

from django.shortcuts import render

from db.database import get_connection


def error_list(request):
    """Отобразить список всех ошибок из базы данных SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        errors = conn.execute(
            """
            SELECT
                errors.id,
                errors.title,
                errors.severity,
                errors.priority,
                statuses.name AS status,
                statuses.name AS status_name,
                developers.name AS developer,
                developers.name AS developer_name,
                users.name AS user,
                users.name AS user_name
            FROM errors
            JOIN statuses ON errors.status_id = statuses.id
            JOIN developers ON errors.developer_id = developers.id
            JOIN users ON errors.user_id = users.id
            ORDER BY errors.id
            """
        ).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "errors/error_list.html",
        {"errors": errors},
    )


def error_detail(request, error_id: int):
    """Отобразить карточку конкретной ошибки из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        error = conn.execute(
            """
            SELECT
                errors.id,
                errors.title,
                errors.description,
                errors.severity,
                errors.priority,
                statuses.name AS status,
                statuses.name AS status_name,
                developers.name AS developer,
                developers.name AS developer_name,
                users.name AS user,
                users.name AS user_name
            FROM errors
            JOIN statuses ON errors.status_id = statuses.id
            JOIN developers ON errors.developer_id = developers.id
            JOIN users ON errors.user_id = users.id
            WHERE errors.id = ?
            """,
            (error_id,),
        ).fetchone()
    finally:
        conn.close()

    return render(
        request,
        "errors/error_detail.html",
        {"error": error},
        status=404 if error is None else 200,
    )


def error_search(request):
    """Поиск ошибок по уровню серьезности через параметризованный SQL."""
    severity = request.GET.get("severity", "").strip()
    errors = []
    if severity:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        try:
            errors = conn.execute(
                """
                SELECT
                    errors.id,
                    errors.title,
                    errors.description,
                    errors.severity,
                    errors.priority,
                    statuses.name AS status,
                    statuses.name AS status_name,
                    developers.name AS developer,
                    developers.name AS developer_name,
                    users.name AS user,
                    users.name AS user_name
                FROM errors
                JOIN statuses ON errors.status_id = statuses.id
                JOIN developers ON errors.developer_id = developers.id
                JOIN users ON errors.user_id = users.id
                WHERE errors.severity = ?
                ORDER BY errors.id
                """,
                [severity],
            ).fetchall()
        finally:
            conn.close()

    return render(
        request,
        "errors/error_search.html",
        {
            "errors": errors,
            "severity": severity,
        },
    )


def statistics(request):
    """Отобразить агрегированную статистику с GROUP BY и HAVING."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        dev_stats = conn.execute(
            """
            SELECT
                developers.name AS developer_name,
                developers.specialization,
                COUNT(errors.id) AS errors_count
            FROM developers
            LEFT JOIN errors ON developers.id = errors.developer_id
            GROUP BY developers.id, developers.name, developers.specialization
            ORDER BY errors_count DESC
            """
        ).fetchall()

        status_stats = conn.execute(
            """
            SELECT
                statuses.name AS status_name,
                COUNT(errors.id) AS errors_count
            FROM statuses
            LEFT JOIN errors ON statuses.id = errors.status_id
            GROUP BY statuses.id, statuses.name
            ORDER BY statuses.id
            """
        ).fetchall()

        busy_devs = conn.execute(
            """
            SELECT
                developers.name AS developer_name,
                COUNT(errors.id) AS errors_count
            FROM developers
            JOIN errors ON developers.id = errors.developer_id
            GROUP BY developers.id, developers.name
            HAVING COUNT(errors.id) > 1
            ORDER BY errors_count DESC
            """
        ).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "errors/statistics.html",
        {
            "dev_stats": dev_stats,
            "status_stats": status_stats,
            "busy_devs": busy_devs,
        },
    )
