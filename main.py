from datetime import date


def validate_error_title(title):
    """Проверяет, что заголовок ошибки заполнен."""
    if title.strip():
        return "Заголовок ошибки заполнен"
    return "Ошибка: укажите заголовок"


def determine_priority(severity):
    """Определяет приоритет ошибки по ее серьезности."""
    normalized_severity = severity.lower()
    if normalized_severity == "критическая":
        return "Высокий"
    if normalized_severity == "значительная":
        return "Средний"
    return "Низкий"


def format_error_report(title, description, severity, status):
    """Формирует краткую карточку зарегистрированной ошибки."""
    registration_date = date.today().isoformat()
    priority = determine_priority(severity)
    return (
        f"Дата регистрации: {registration_date}\n"
        f"Заголовок: {title}\n"
        f"Описание: {description}\n"
        f"Серьезность: {severity}\n"
        f"Приоритет: {priority}\n"
        f"Статус: {status}"
    )


def main():
    error_title = "Ошибка авторизации при неверном пароле"
    error_description = "После пяти неверных попыток пользователь не получает сообщение блокировки."
    error_severity = "значительная"
    error_status = "Новая"

    print("СЕРВИС УЧЕТА ОШИБОК ПРОГРАММНОГО ПРОДУКТА")
    print(validate_error_title(error_title))
    print(format_error_report(
        error_title,
        error_description,
        error_severity,
        error_status,
    ))


if __name__ == "__main__":
    main()
