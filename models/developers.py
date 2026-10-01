"""Класс разработчика сервиса."""

from typing import Any, Dict


class Developer:
    """Разработчик, ответственный за исправление ошибки."""

    def __init__(
        self, developer_id: int, name: str, specialization: str
    ) -> None:
        """Создать разработчика."""
        self.id = developer_id
        self.name = name
        self.specialization = specialization

    def __str__(self) -> str:
        """Вернуть имя и специализацию разработчика."""
        return f"{self.name} ({self.specialization})"

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Developer":
        """Создать разработчика из JSON-словаря."""
        return cls(data["id"], data["name"], data["specialization"])

    def to_data(self) -> Dict[str, Any]:
        """Преобразовать разработчика в JSON-словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
        }
