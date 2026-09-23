"""Класс статуса ошибки."""

from typing import Any, Dict


class Status:
    """Статус обработки ошибки."""

    def __init__(self, status_id: int, name: str) -> None:
        """Создать статус."""
        self.id = status_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть название статуса."""
        return self.name

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Status":
        """Создать статус из JSON-словаря."""
        return cls(data["id"], data["name"])

    def to_data(self) -> Dict[str, Any]:
        """Преобразовать статус в JSON-словарь."""
        return {"id": self.id, "name": self.name}
