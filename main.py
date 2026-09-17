"""Консольный интерфейс сервиса учета ошибок."""

from datetime import date
from pathlib import Path
from typing import List

from errors import (
    Error,
    add_error,
    delete_error,
    determine_priority,
    find_errors,
    filter_errors_by_severity,
    filter_errors_by_status,
    sort_errors,
    update_error_status,
)
from entities import Developer, Status, User
from storage import (
    load_developers,
    load_errors,
    load_statuses,
    load_users,
    save_errors,
)
from utils import input_int


def validate_error_title(title: str) -> str:
    """Проверить, что заголовок ошибки заполнен."""
    if title.strip():
        return "Заголовок ошибки заполнен"
    return "Ошибка: укажите заголовок"


def format_error_report(
    title: str, description: str, severity: str, status: str
) -> str:
    """Сформировать краткую карточку зарегистрированной ошибки."""
    registration_date = date.today().isoformat()
    return (
        f"Дата регистрации: {registration_date}\n"
        f"Заголовок: {title}\n"
        f"Описание: {description}\n"
        f"Серьезность: {severity}\n"
        f"Приоритет: {determine_priority(severity)}\n"
        f"Статус: {status}"
    )


def show_errors(
    errors: List[Error],
    users: List[User],
    developers: List[Developer],
) -> None:
    """Вывести список ошибок, отсортированный по приоритету."""
    if not errors:
        print("Ошибки не найдены.")
        return
    for error in sort_errors(errors):
        user = next(
            (item for item in users if item["id"] == error["user_id"]),
            {"name": "Неизвестный пользователь"},
        )
        developer = next(
            (
                item
                for item in developers
                if item["id"] == error["developer_id"]
            ),
            {"name": "Разработчик не назначен"},
        )
        print(
            f"{error['id']}. {error['title']} | "
            f"{error['severity']} | {error['priority']} | "
            f"{error['status']}"
        )
        print(
            f"   {error['description']} | "
            f"Пользователь: {user['name']} | "
            f"Разработчик: {developer['name']}"
        )


def _data_path() -> Path:
    """Вернуть путь к файлу с ошибками."""
    return Path(__file__).parent / "data" / "errors.json"


def _reference_paths() -> tuple[Path, Path, Path]:
    """Вернуть пути к справочникам пользователей, разработчиков и статусов."""
    data_dir = Path(__file__).parent / "data"
    return (
        data_dir / "users.json",
        data_dir / "developers.json",
        data_dir / "statuses.json",
    )


def _print_menu() -> None:
    """Вывести меню приложения."""
    print(
        "\n=== Сервис учета ошибок программного продукта ===\n"
        "1. Показать все ошибки\n"
        "2. Найти ошибку\n"
        "3. Добавить ошибку\n"
        "4. Фильтр по статусу\n"
        "5. Фильтр по серьезности\n"
        "6. Изменить статус\n"
        "7. Удалить ошибку\n"
        "0. Выход"
    )


def _add_error_from_input(
    errors: List[Error],
    users: List[User],
    developers: List[Developer],
    statuses: List[Status],
) -> None:
    """Получить данные ошибки из консоли и добавить запись."""
    title = input("Заголовок: ")
    description = input("Описание: ")
    severity = input("Серьезность (критическая/значительная/незначительная): ")
    user_id = input_int("ID пользователя: ")
    developer_id = input_int("ID разработчика: ")
    status = input("Статус: ") or statuses[0]["name"]
    if not any(item["id"] == user_id for item in users):
        raise ValueError("Пользователь не найден")
    if not any(item["id"] == developer_id for item in developers):
        raise ValueError("Разработчик не найден")
    if not any(item["name"] == status for item in statuses):
        raise ValueError("Статус не найден")
    error = add_error(
        errors,
        title,
        description,
        severity,
        status,
        user_id,
        developer_id,
    )
    print(f"Ошибка зарегистрирована с ID {error['id']}.")


def main() -> None:
    """Запустить цикл меню и сохранить изменения перед выходом."""
    errors_file = _data_path()
    users_file, developers_file, statuses_file = _reference_paths()
    errors = load_errors(errors_file)
    users = load_users(users_file)
    developers = load_developers(developers_file)
    statuses = load_statuses(statuses_file)

    while True:
        _print_menu()
        choice = input_int("\nВыберите действие: ")
        try:
            if choice == 0:
                save_errors(errors_file, errors)
                print("Данные сохранены. До свидания!")
                return
            if choice == 1:
                show_errors(errors, users, developers)
            elif choice == 2:
                show_errors(
                    find_errors(errors, input("Поисковый запрос: ")),
                    users,
                    developers,
                )
            elif choice == 3:
                _add_error_from_input(errors, users, developers, statuses)
                save_errors(errors_file, errors)
            elif choice == 4:
                show_errors(
                    filter_errors_by_status(errors, input("Статус: ")),
                    users,
                    developers,
                )
            elif choice == 5:
                show_errors(
                    filter_errors_by_severity(errors, input("Серьезность: ")),
                    users,
                    developers,
                )
            elif choice == 6:
                error_id = input_int("ID ошибки: ")
                status = input("Новый статус: ")
                if update_error_status(errors, error_id, status):
                    save_errors(errors_file, errors)
                    print("Статус изменен.")
                else:
                    print("Ошибка не найдена.")
            elif choice == 7:
                error_id = input_int("ID ошибки: ")
                if delete_error(errors, error_id):
                    save_errors(errors_file, errors)
                    print("Ошибка удалена.")
                else:
                    print("Ошибка не найдена.")
            else:
                print("Ошибка: выберите пункт из меню.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
