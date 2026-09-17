"""Типизированные сущности сервиса учета ошибок."""

from typing import List, TypedDict


class User(TypedDict):
    """Пользователь, зарегистрировавший ошибку."""

    id: int
    name: str
    email: str


class Developer(TypedDict):
    """Разработчик, ответственный за исправление ошибки."""

    id: int
    name: str
    specialization: str


class Status(TypedDict):
    """Допустимый статус обработки ошибки."""

    id: int
    name: str


def add_user(users: List[User], name: str, email: str) -> User:
    """Добавить пользователя в справочник."""
    if not name.strip() or not email.strip():
        raise ValueError("Имя и электронная почта пользователя обязательны")
    user: User = {
        "id": max((item["id"] for item in users), default=0) + 1,
        "name": name.strip(),
        "email": email.strip(),
    }
    users.append(user)
    return user


def add_developer(
    developers: List[Developer], name: str, specialization: str
) -> Developer:
    """Добавить разработчика в справочник."""
    if not name.strip() or not specialization.strip():
        raise ValueError("Имя и специализация разработчика обязательны")
    developer: Developer = {
        "id": max((item["id"] for item in developers), default=0) + 1,
        "name": name.strip(),
        "specialization": specialization.strip(),
    }
    developers.append(developer)
    return developer


def add_status(statuses: List[Status], name: str) -> Status:
    """Добавить статус в справочник."""
    if not name.strip():
        raise ValueError("Название статуса не может быть пустым")
    status: Status = {
        "id": max((item["id"] for item in statuses), default=0) + 1,
        "name": name.strip(),
    }
    statuses.append(status)
    return status
