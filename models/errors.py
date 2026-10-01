"""Класс ошибки программного продукта."""

from typing import Any, Dict, Optional

from .developers import Developer
from .statuses import Status
from .users import User


class Error:
    """Ошибка с ответственными пользователем и разработчиком."""

    def __init__(
        self,
        error_id: int,
        title: str,
        description: str,
        severity: str,
        priority: str,
        status: Status,
        user: User,
        developer: Developer,
    ) -> None:
        """Создать объект ошибки."""
        self.id = error_id
        self.title = title
        self.description = description
        self.severity = severity
        self.priority = priority
        self.status = status
        self.user = user
        self.developer = developer

    def __str__(self) -> str:
        """Вернуть краткое представление ошибки."""
        return (
            f"{self.id}. {self.title} | {self.severity} | "
            f"{self.priority} | {self.status}"
        )

    @classmethod
    def from_data(
        cls,
        data: Dict[str, Any],
        users: list[User],
        developers: list[Developer],
        statuses: list[Status],
    ) -> Optional["Error"]:
        """Создать ошибку и восстановить связи со справочниками."""
        user = next(
            (item for item in users if item.id == data["user_id"]),
            None,
        )
        developer = next(
            (item for item in developers if item.id == data["developer_id"]),
            None,
        )
        status = next(
            (item for item in statuses if item.name == data["status"]),
            None,
        )
        if user is None or developer is None or status is None:
            return None
        return cls(
            data["id"],
            data["title"],
            data["description"],
            data["severity"],
            data["priority"],
            status,
            user,
            developer,
        )

    def to_data(self) -> Dict[str, Any]:
        """Преобразовать ошибку в JSON-словарь со ссылками по ID."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "priority": self.priority,
            "status": self.status.name,
            "user_id": self.user.id,
            "developer_id": self.developer.id,
        }
