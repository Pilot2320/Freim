"""Представление главной страницы с выборкой показателей через Django ORM."""

from django.shortcuts import render

from bugtracker.models import Error


def _load_error_context() -> dict:
    total = Error.objects.count()
    open_errors = Error.objects.exclude(status__name="Закрыта").count()
    high_priority = Error.objects.filter(priority="Высокий").count()
    recent = (
        Error.objects.select_related("status", "developer", "user")
        .order_by("-id")[:5]
    )
    return {
        "errors": recent,
        "total_errors": total,
        "open_errors": open_errors,
        "high_priority": high_priority,
    }


def home(request):
    """Главная страница сервиса."""
    context = _load_error_context()
    return render(request, "homepage/index.html", context)


def index(request):
    """Алиас представления главной страницы."""
    return home(request)
