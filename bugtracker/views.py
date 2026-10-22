from pathlib import Path

from django.shortcuts import render

from errors import sort_errors
from storage import load_developers, load_errors, load_statuses, load_users


def _load_error_list():
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    users = load_users(data_dir / "users.json")
    developers = load_developers(data_dir / "developers.json")
    statuses = load_statuses(data_dir / "statuses.json")
    return sort_errors(
        load_errors(data_dir / "errors.json", users, developers, statuses)
    )


def error_list(request):
    errors = _load_error_list()
    return render(
        request,
        "errors/error_list.html",
        {"errors": errors},
    )


def error_detail(request, error_id):
    errors = _load_error_list()
    error = next((item for item in errors if item.id == error_id), None)
    return render(
        request,
        "errors/error_detail.html",
        {"error": error},
        status=404 if error is None else 200,
    )
