"""Вспомогательные функции безопасного пользовательского ввода."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число и повторять запрос при ошибке."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ и повторять запрос при ошибке."""
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: используйте формат ДД.ММ.ГГГГ.")
