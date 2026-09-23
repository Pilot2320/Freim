import json

from models import Developer, Error, Status, User
from storage import load_errors, save_errors


def test_model_creation_and_string_representation():
    user = User(1, "Иван", "ivan@example.com")
    developer = Developer(1, "Анна", "Backend")
    status = Status(1, "Новая")
    error = Error(
        1,
        "Ошибка входа",
        "Описание",
        "критическая",
        "Высокий",
        status,
        user,
        developer,
    )

    assert str(user) == "Иван <ivan@example.com>"
    assert str(developer) == "Анна (Backend)"
    assert str(status) == "Новая"
    assert "Ошибка входа" in str(error)


def test_error_json_round_trip(tmp_path):
    user = User(1, "Иван", "ivan@example.com")
    developer = Developer(1, "Анна", "Backend")
    status = Status(1, "Новая")
    error = Error(
        1,
        "Ошибка входа",
        "Описание",
        "критическая",
        "Высокий",
        status,
        user,
        developer,
    )
    filename = tmp_path / "errors.json"

    save_errors(filename, [error])
    data = json.loads(filename.read_text(encoding="utf-8"))
    loaded = load_errors(filename, [user], [developer], [status])

    assert data[0]["user_id"] == 1
    assert loaded[0].user is user
    assert loaded[0].developer is developer
    assert loaded[0].status is status
