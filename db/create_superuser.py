"""Скрипт создания суперпользователя Django для административной панели."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freim_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402


def ensure_superuser(
    username="admin", email="admin@example.com", password="admin"
):
    """Создаёт суперпользователя, если он ещё не существует."""
    user_cls = get_user_model()
    if not user_cls.objects.filter(username=username).exists():
        user_cls.objects.create_superuser(username, email, password)
        print(f"Суперпользователь '{username}' успешно создан.")
    else:
        print(f"Суперпользователь '{username}' уже существует.")


if __name__ == "__main__":
    ensure_superuser()
