import pytest

from errors import (
    add_error,
    delete_error,
    determine_priority,
    find_errors,
    sort_errors,
    update_error_status,
)
from models import Developer, Status, User


def make_context():
    """Создать связанные объекты для тестов ошибок."""
    return (
        User(1, "Иван", "ivan@example.com"),
        Developer(1, "Анна", "Backend"),
        Status(1, "Новая"),
    )


def test_add_error_and_priority():
    errors = []
    user, developer, status = make_context()
    error = add_error(
        errors,
        "Ошибка входа",
        "Не открывается форма",
        "критическая",
        status,
        user,
        developer,
    )

    assert error.id == 1
    assert error.priority == "Высокий"
    assert error.user is user
    assert error.developer is developer


def test_find_error():
    errors = []
    user, developer, status = make_context()
    add_error(
        errors,
        "Ошибка входа",
        "Не открывается форма",
        "значительная",
        status,
        user,
        developer,
    )

    assert find_errors(errors, "форма")[0].title == "Ошибка входа"


def test_update_and_delete_error():
    errors = []
    user, developer, status = make_context()
    error = add_error(
        errors,
        "Ошибка входа",
        "Описание",
        "незначительная",
        status,
        user,
        developer,
    )
    fixed_status = Status(2, "Исправлена")

    assert update_error_status(errors, error.id, fixed_status)
    assert error.status is fixed_status
    assert delete_error(errors, error.id)
    assert errors == []


def test_sort_errors_by_priority():
    errors = []
    user, developer, status = make_context()
    add_error(
        errors,
        "Низкий",
        "Описание",
        "незначительная",
        status,
        user,
        developer,
    )
    add_error(
        errors,
        "Высокий",
        "Описание",
        "критическая",
        status,
        user,
        developer,
    )

    assert sort_errors(errors)[0].title == "Высокий"


def test_invalid_error_is_rejected():
    user, developer, status = make_context()
    with pytest.raises(ValueError):
        add_error(
            [], "", "Описание", "критическая", status, user, developer
        )

    assert determine_priority("неизвестная") == "Низкий"
