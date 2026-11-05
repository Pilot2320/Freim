"""Скрипт переноса данных из исходной базы SQLite в целевую базу Django ORM."""

import os
from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freim_project.settings")

import django  # noqa: E402
django.setup()

from django.db import transaction  # noqa: E402
from bugtracker.models import Developer, Error, Status, User  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "freim.sqlite"


def main():
    if not SOURCE_DB.exists():
        alt_db = BASE_DIR / "data" / "roomly.sqlite"
        if alt_db.exists():
            source = alt_db
        else:
            raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")
    else:
        source = SOURCE_DB

    with sqlite3.connect(source) as connection:
        connection.row_factory = sqlite3.Row

        users = connection.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()
        developers = connection.execute(
            "SELECT id, name, specialization FROM developers ORDER BY id"
        ).fetchall()
        statuses = connection.execute(
            "SELECT id, name FROM statuses ORDER BY id"
        ).fetchall()
        errors = connection.execute(
            """
            SELECT id, title, description, severity, priority,
                   status_id, user_id, developer_id
            FROM errors
            ORDER BY id
            """
        ).fetchall()

        with transaction.atomic():
            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "email": row["email"],
                    },
                )

            for row in developers:
                Developer.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "specialization": row["specialization"],
                    },
                )

            for row in statuses:
                Status.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                    },
                )

            for row in errors:
                Error.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "title": row["title"],
                        "description": row["description"],
                        "severity": row["severity"],
                        "priority": row["priority"],
                        "status_id": row["status_id"],
                        "user_id": row["user_id"],
                        "developer_id": row["developer_id"],
                    },
                )

    print("Перенос данных завершён.")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Разработчиков: {Developer.objects.count()}")
    print(f"Статусов: {Status.objects.count()}")
    print(f"Ошибок: {Error.objects.count()}")


if __name__ == "__main__":
    main()

