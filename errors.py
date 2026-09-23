"""Функции обработки коллекции объектов Error."""

from typing import List, Optional

from models import Developer, Error, Status, User


DEFAULT_SEVERITIES = {
    1: "критическая",
    2: "значительная",
    3: "незначительная",
}


def determine_priority(severity: str) -> str:
    """Определить приоритет ошибки по уровню серьезности."""
    priorities = {
        "критическая": "Высокий",
        "значительная": "Средний",
        "незначительная": "Низкий",
    }
    return priorities.get(severity.strip().lower(), "Низкий")


def add_error(
    errors: List[Error],
    title: str,
    description: str,
    severity: str,
    status: Status,
    user: User,
    developer: Developer,
) -> Error:
    """Создать объект ошибки и добавить его в коллекцию."""
    if not title.strip():
        raise ValueError("Заголовок ошибки не может быть пустым")
    if not description.strip():
        raise ValueError("Описание ошибки не может быть пустым")

    normalized_severity = severity.strip().lower()
    if normalized_severity not in DEFAULT_SEVERITIES.values():
        raise ValueError("Укажите корректную серьезность ошибки")

    error = Error(
        max((item.id for item in errors), default=0) + 1,
        title.strip(),
        description.strip(),
        normalized_severity,
        determine_priority(normalized_severity),
        status,
        user,
        developer,
    )
    errors.append(error)
    return error


def find_errors(errors: List[Error], query: str) -> List[Error]:
    """Найти объекты ошибок по заголовку или описанию."""
    normalized_query = query.strip().lower()
    return [
        error
        for error in errors
        if normalized_query in error.title.lower()
        or normalized_query in error.description.lower()
    ]


def filter_errors_by_status(
    errors: List[Error], status: Status
) -> List[Error]:
    """Отобрать ошибки с указанным объектом статуса."""
    return [error for error in errors if error.status.id == status.id]


def filter_errors_by_severity(
    errors: List[Error], severity: str
) -> List[Error]:
    """Отобрать ошибки указанной серьезности."""
    normalized_severity = severity.strip().lower()
    return [error for error in errors if error.severity == normalized_severity]


def sort_errors(errors: List[Error]) -> List[Error]:
    """Отсортировать ошибки от самых приоритетных к менее приоритетным."""
    priority_order = {"Высокий": 0, "Средний": 1, "Низкий": 2}
    return sorted(
        errors,
        key=lambda error: (priority_order.get(error.priority, 3), error.id),
    )


def update_error_status(
    errors: List[Error], error_id: int, status: Status
) -> bool:
    """Изменить статус ошибки по идентификатору."""
    for error in errors:
        if error.id == error_id:
            error.status = status
            return True
    return False


def delete_error(errors: List[Error], error_id: int) -> bool:
    """Удалить ошибку по идентификатору."""
    for index, error in enumerate(errors):
        if error.id == error_id:
            del errors[index]
            return True
    return False


def find_by_id(errors: List[Error], error_id: int) -> Optional[Error]:
    """Найти ошибку по идентификатору."""
    return next((error for error in errors if error.id == error_id), None)
