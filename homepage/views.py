from pathlib import Path

from django.shortcuts import render

from errors import sort_errors
from storage import load_developers, load_errors, load_statuses, load_users


def _load_error_context() -> dict:
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    users = load_users(data_dir / "users.json")
    developers = load_developers(data_dir / "developers.json")
    statuses = load_statuses(data_dir / "statuses.json")
    errors = load_errors(data_dir / "errors.json", users, developers, statuses)
    open_count = sum(
        1 for error in errors if error.status.name != "Закрыта"
    )
    high_count = sum(
        1 for error in errors if error.priority == "Высокий"
    )
    return {
        "errors": sort_errors(errors),
        "total_errors": len(errors),
        "open_errors": open_count,
        "high_priority": high_count,
    }


def home(request):
    context = _load_error_context()
    return render(request, "homepage/index.html", context)


def index(request):
    return home(request)
