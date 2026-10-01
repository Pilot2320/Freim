"""Консольный интерфейс объектного сервиса учета ошибок."""

from datetime import date
from pathlib import Path
from typing import List

from errors import (
    DEFAULT_SEVERITIES,
    add_error,
    delete_error,
    determine_priority,
    filter_errors_by_severity,
    filter_errors_by_status,
    find_errors,
    sort_errors,
    update_error_status,
)
from models import Developer, Error, Status, User
from storage import (
    load_developers,
    load_errors,
    load_statuses,
    load_users,
    save_developers,
    save_errors,
    save_statuses,
    save_users,
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


def show_errors(errors: List[Error]) -> None:
    """Вывести список объектов ошибок."""
    if not errors:
        print("Ошибки не найдены.")
        return
    for error in sort_errors(errors):
        print(error)
        print(
            f"   {error.description} | Пользователь: {error.user} | "
            f"Разработчик: {error.developer}"
        )


def _data_paths() -> tuple[Path, Path, Path, Path]:
    """Вернуть пути к файлам объектных данных."""
    data_dir = Path(__file__).parent / "data"
    return (
        data_dir / "errors.json",
        data_dir / "users.json",
        data_dir / "developers.json",
        data_dir / "statuses.json",
    )


def _print_menu() -> None:
    """Вывести главное меню приложения."""
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


def _select_status(statuses: List[Status]) -> Status:
    """Выбрать объект статуса по ID."""
    print("Доступные статусы:")
    for status in statuses:
        print(f"{status.id}. {status.name}")
    status_id = input_int("ID статуса: ")
    selected = next((item for item in statuses if item.id == status_id), None)
    if selected is None:
        raise ValueError("Статус не найден")
    return selected


def _select_severity() -> str:
    """Выбрать серьезность по числовому ID."""
    print("Уровни серьезности:")
    for severity_id, severity in DEFAULT_SEVERITIES.items():
        print(f"{severity_id}. {severity}")
    selected_severity: str | None = DEFAULT_SEVERITIES.get(
        input_int("ID серьезности: ")
    )
    if selected_severity is None:
        raise ValueError("Уровень серьезности не найден")
    return selected_severity


def _add_error_from_input(
    errors: List[Error],
    users: List[User],
    developers: List[Developer],
    statuses: List[Status],
) -> None:
    """Получить данные и создать связанную ошибку."""
    title = input("Заголовок: ")
    description = input("Описание: ")
    severity = _select_severity()
    user_id = input_int("ID пользователя: ")
    developer_id = input_int("ID разработчика: ")
    user = next((item for item in users if item.id == user_id), None)
    developer = next(
        (item for item in developers if item.id == developer_id), None
    )
    if user is None:
        raise ValueError("Пользователь не найден")
    if developer is None:
        raise ValueError("Разработчик не найден")
    status = _select_status(statuses)
    error = add_error(
        errors, title, description, severity, status, user, developer
    )
    print(f"Ошибка зарегистрирована с ID {error.id}.")


def _save_all(
    paths: tuple[Path, Path, Path, Path],
    errors: List[Error],
    users: List[User],
    developers: List[Developer],
    statuses: List[Status],
) -> None:
    """Сохранить все коллекции объектной модели."""
    errors_file, users_file, developers_file, statuses_file = paths
    save_errors(errors_file, errors)
    save_users(users_file, users)
    save_developers(developers_file, developers)
    save_statuses(statuses_file, statuses)


def main() -> None:
    """Загрузить объекты, запустить меню и сохранить изменения."""
    paths = _data_paths()
    errors_file, users_file, developers_file, statuses_file = paths
    users = load_users(users_file)
    developers = load_developers(developers_file)
    statuses = load_statuses(statuses_file)
    errors = load_errors(errors_file, users, developers, statuses)

    while True:
        _print_menu()
        choice = input_int("\nВыберите действие: ")
        try:
            if choice == 0:
                _save_all(paths, errors, users, developers, statuses)
                print("Данные сохранены. До свидания!")
                return
            if choice == 1:
                show_errors(errors)
            elif choice == 2:
                show_errors(find_errors(errors, input("Поисковый запрос: ")))
            elif choice == 3:
                _add_error_from_input(errors, users, developers, statuses)
                save_errors(errors_file, errors)
            elif choice == 4:
                show_errors(errors)
                status = _select_status(statuses)
                show_errors(filter_errors_by_status(errors, status))
            elif choice == 5:
                show_errors(
                    filter_errors_by_severity(errors, _select_severity())
                )
            elif choice == 6:
                error_id = input_int("ID ошибки: ")
                status = _select_status(statuses)
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
