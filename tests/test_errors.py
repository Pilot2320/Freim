import pytest

from errors import (
    add_error,
    delete_error,
    determine_priority,
    find_errors,
    sort_errors,
    update_error_status,
)


def test_add_error_and_priority():
    errors = []
    error = add_error(
        errors, "Ошибка входа", "Не открывается форма", "критическая"
    )

    assert error["id"] == 1
    assert error["priority"] == "Высокий"


def test_find_error():
    errors = []
    add_error(errors, "Ошибка входа", "Не открывается форма", "значительная")

    assert find_errors(errors, "форма")[0]["title"] == "Ошибка входа"


def test_update_and_delete_error():
    errors = []
    add_error(errors, "Ошибка входа", "Описание", "незначительная")

    assert update_error_status(errors, 1, "Исправлена")
    assert errors[0]["status"] == "Исправлена"
    assert delete_error(errors, 1)
    assert errors == []


def test_sort_errors_by_priority():
    errors = []
    add_error(errors, "Низкий", "Описание", "незначительная")
    add_error(errors, "Высокий", "Описание", "критическая")

    assert sort_errors(errors)[0]["title"] == "Высокий"


def test_invalid_error_is_rejected():
    with pytest.raises(ValueError):
        add_error([], "", "Описание", "критическая")

    assert determine_priority("неизвестная") == "Низкий"
