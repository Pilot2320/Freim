"""Класс пользователя сервиса."""

from typing import Any, Dict


class User:
    """Пользователь, зарегистрировавший ошибку."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть имя и электронную почту пользователя."""
        return f"{self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "User":
        """Создать пользователя из JSON-словаря."""
        return cls(data["id"], data["name"], data["email"])

    def to_data(self) -> Dict[str, Any]:
        """Преобразовать пользователя в JSON-словарь."""
        return {"id": self.id, "name": self.name, "email": self.email}
