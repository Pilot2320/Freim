"""Функции для работы с ошибками программного продукта."""

from typing import Dict, List


Error = Dict[str, object]


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
    status: str = "Новая",
) -> Error:
    """Добавить ошибку в список и вернуть созданную запись."""
    if not title.strip():
        raise ValueError("Заголовок ошибки не может быть пустым")
    if not description.strip():
        raise ValueError("Описание ошибки не может быть пустым")

    normalized_severity = severity.strip().lower()
    if normalized_severity not in {
        "критическая",
        "значительная",
        "незначительная",
    }:
        raise ValueError("Укажите корректную серьезность ошибки")

    error = {
        "id": max((int(item["id"]) for item in errors), default=0) + 1,
        "title": title.strip(),
        "description": description.strip(),
        "severity": normalized_severity,
        "priority": determine_priority(normalized_severity),
        "status": status.strip() or "Новая",
    }
    errors.append(error)
    return error


def find_errors(errors: List[Error], query: str) -> List[Error]:
    """Найти ошибки по подстроке в заголовке или описании."""
    normalized_query = query.strip().lower()
    return [
        error
        for error in errors
        if normalized_query in str(error["title"]).lower()
        or normalized_query in str(error["description"]).lower()
    ]


def filter_errors_by_status(errors: List[Error], status: str) -> List[Error]:
    """Отобрать ошибки с указанным статусом."""
    return [error for error in errors if error["status"] == status]


def filter_errors_by_severity(
    errors: List[Error], severity: str
) -> List[Error]:
    """Отобрать ошибки указанной серьезности."""
    normalized_severity = severity.strip().lower()
    return [
        error for error in errors if error["severity"] == normalized_severity
    ]


def sort_errors(errors: List[Error]) -> List[Error]:
    """Отсортировать ошибки от самых приоритетных к менее приоритетным."""
    priority_order = {"Высокий": 0, "Средний": 1, "Низкий": 2}
    return sorted(
        errors,
        key=lambda error: (
            priority_order.get(str(error["priority"]), 3),
            error["id"],
        ),
    )


def update_error_status(
    errors: List[Error], error_id: int, status: str
) -> bool:
    """Изменить статус ошибки по идентификатору."""
    if not status.strip():
        raise ValueError("Статус не может быть пустым")
    for error in errors:
        if int(error["id"]) == error_id:
            error["status"] = status.strip()
            return True
    return False


def delete_error(errors: List[Error], error_id: int) -> bool:
    """Удалить ошибку по идентификатору."""
    for index, error in enumerate(errors):
        if int(error["id"]) == error_id:
            del errors[index]
            return True
    return False
