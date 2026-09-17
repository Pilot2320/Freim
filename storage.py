"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
from pathlib import Path
from typing import List, Union

from errors import Error
from entities import Developer, Status, User


def _read_json(filename: Union[str, Path], default: object) -> object:
    """Прочитать JSON и вернуть значение по умолчанию при ошибке файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def load_errors(filename: Union[str, Path]) -> List[Error]:
    """Загрузить ошибки из JSON-файла."""
    data = _read_json(filename, [])
    return data if isinstance(data, list) else []


def save_errors(filename: Union[str, Path], errors: List[Error]) -> None:
    """Сохранить список ошибок в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(errors, file, ensure_ascii=False, indent=2)


def load_users(filename: Union[str, Path]) -> List[User]:
    """Загрузить пользователей из JSON-файла."""
    data = _read_json(filename, [])
    return data if isinstance(data, list) else []


def load_developers(filename: Union[str, Path]) -> List[Developer]:
    """Загрузить разработчиков из JSON-файла."""
    data = _read_json(filename, [])
    return data if isinstance(data, list) else []


def load_statuses(filename: Union[str, Path]) -> List[Status]:
    """Загрузить статусы из JSON-файла."""
    data = _read_json(filename, [])
    return data if isinstance(data, list) else []
