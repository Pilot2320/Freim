"""Загрузка и сохранение объектной модели в JSON."""

import json
from pathlib import Path
from typing import Any, List, Protocol, Type, TypeVar, Union

from models import Developer, Error, Status, User


PathLike = Union[str, Path]
Model = TypeVar("Model")


class DataModel(Protocol):
    """Протокол объекта, который можно создать из JSON."""

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Any:
        """Создать объект из словаря."""
        ...


def _read_json(filename: PathLike, default: Any) -> Any:
    """Прочитать JSON и вернуть значение по умолчанию при ошибке."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _load_simple(
    filename: PathLike, model: Type[DataModel]
) -> List[Model]:
    """Загрузить список объектов с методом from_data()."""
    data = _read_json(filename, [])
    if not isinstance(data, list):
        return []
    return [model.from_data(item) for item in data]


def load_users(filename: PathLike) -> List[User]:
    """Загрузить пользователей как объекты User."""
    return _load_simple(filename, User)


def load_developers(filename: PathLike) -> List[Developer]:
    """Загрузить разработчиков как объекты Developer."""
    return _load_simple(filename, Developer)


def load_statuses(filename: PathLike) -> List[Status]:
    """Загрузить статусы как объекты Status."""
    return _load_simple(filename, Status)


def load_errors(
    filename: PathLike,
    users: List[User],
    developers: List[Developer],
    statuses: List[Status],
) -> List[Error]:
    """Загрузить ошибки и восстановить связи между объектами."""
    data = _read_json(filename, [])
    if not isinstance(data, list):
        return []
    errors = []
    for item in data:
        error = Error.from_data(item, users, developers, statuses)
        if error is not None:
            errors.append(error)
    return errors


def _save_simple(filename: PathLike, objects: List[Any]) -> None:
    """Сохранить объекты, преобразовав их в JSON-словари."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [item.to_data() for item in objects],
            file,
            ensure_ascii=False,
            indent=2,
        )


def save_users(filename: PathLike, users: List[User]) -> None:
    """Сохранить пользователей."""
    _save_simple(filename, users)


def save_developers(
    filename: PathLike, developers: List[Developer]
) -> None:
    """Сохранить разработчиков."""
    _save_simple(filename, developers)


def save_statuses(filename: PathLike, statuses: List[Status]) -> None:
    """Сохранить статусы."""
    _save_simple(filename, statuses)


def save_errors(filename: PathLike, errors: List[Error]) -> None:
    """Сохранить ошибки со ссылками на связанные объекты по ID."""
    _save_simple(filename, errors)
