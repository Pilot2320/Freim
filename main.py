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
from storage import load_errors, save_errors
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
    """Вывести список ошибок, отсортированный по приоритету."""
    if not errors:
        print("Ошибки не найдены.")
        return
    for error in sort_errors(errors):
        print(
            f"{error['id']}. {error['title']} | "
            f"{error['severity']} | {error['priority']} | {error['status']}"
        )
        print(f"   {error['description']}")


def _data_path() -> Path:
    """Вернуть путь к файлу с ошибками."""
    return Path(__file__).parent / "data" / "errors.json"


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


def _add_error_from_input(errors: List[Error]) -> None:
    """Получить данные ошибки из консоли и добавить запись."""
    title = input("Заголовок: ")
    description = input("Описание: ")
    severity = input("Серьезность (критическая/значительная/незначительная): ")
    error = add_error(errors, title, description, severity)
    print(f"Ошибка зарегистрирована с ID {error['id']}.")


def main() -> None:
    """Запустить цикл меню и сохранить изменения перед выходом."""
    errors_file = _data_path()
    errors = load_errors(errors_file)

    while True:
        _print_menu()
        choice = input_int("\nВыберите действие: ")
        try:
            if choice == 0:
                save_errors(errors_file, errors)
                print("Данные сохранены. До свидания!")
                return
            if choice == 1:
                show_errors(errors)
            elif choice == 2:
                show_errors(find_errors(errors, input("Поисковый запрос: ")))
            elif choice == 3:
                _add_error_from_input(errors)
                save_errors(errors_file, errors)
            elif choice == 4:
                show_errors(filter_errors_by_status(errors, input("Статус: ")))
            elif choice == 5:
                show_errors(
                    filter_errors_by_severity(errors, input("Серьезность: "))
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
