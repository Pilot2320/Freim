from main import determine_priority, format_error_report, validate_error_title


def test_validate_error_title():
    assert validate_error_title("Ошибка входа") == "Заголовок ошибки заполнен"
    assert validate_error_title("   ") == "Ошибка: укажите заголовок"


def test_determine_priority():
    assert determine_priority("критическая") == "Высокий"
    assert determine_priority("значительная") == "Средний"
    assert determine_priority("незначительная") == "Низкий"


def test_format_error_report():
    report = format_error_report(
        "Ошибка входа",
        "Не отображается сообщение об ошибке.",
        "значительная",
        "Новая",
    )

    assert "Заголовок: Ошибка входа" in report
    assert "Приоритет: Средний" in report
    assert "Статус: Новая" in report
