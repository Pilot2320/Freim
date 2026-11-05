"""Представления для работы с ошибками через Django ORM (ПР9)."""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Developer, Error, Status, User


def error_list(request):
    """Список ошибок с фильтрацией, сортировкой и пагинацией (ORM)."""
    severity = request.GET.get("severity", "").strip()
    priority = request.GET.get("priority", "").strip()
    status_id = request.GET.get("status", "").strip()
    dev_id = request.GET.get("developer", "").strip()
    sort = request.GET.get("sort", "id").strip()

    errors_qs = Error.objects.select_related("status", "developer", "user")

    if severity:
        errors_qs = errors_qs.filter(severity=severity)
    if priority:
        errors_qs = errors_qs.filter(priority=priority)
    if status_id.isdigit():
        errors_qs = errors_qs.filter(status_id=int(status_id))
    if dev_id.isdigit():
        errors_qs = errors_qs.filter(developer_id=int(dev_id))

    sort_fields = {
        "id": "id",
        "-id": "-id",
        "title": "title",
        "severity": "severity",
        "priority": "priority",
        "status": "status__name",
        "developer": "developer__name",
    }
    sort_field = sort_fields.get(sort, "id")
    errors_qs = errors_qs.order_by(sort_field)

    paginator = Paginator(errors_qs, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "errors": page_obj,
        "page_obj": page_obj,
        "total_count": errors_qs.count(),
        "statuses": Status.objects.order_by("id"),
        "developers": Developer.objects.order_by("name"),
        "users": User.objects.order_by("name"),
        "selected_severity": severity,
        "selected_priority": priority,
        "selected_status": status_id,
        "selected_dev": dev_id,
        "selected_sort": sort,
    }
    return render(request, "errors/error_list.html", context)


def error_detail(request, error_id: int):
    """Карточка отдельной ошибки, полученная через get_object_or_404."""
    error = get_object_or_404(
        Error.objects.select_related("status", "developer", "user"),
        pk=error_id,
    )
    return render(
        request,
        "errors/error_detail.html",
        {"error": error},
    )


def error_search(request):
    """Поиск ошибок по уровню серьезности или запросу через Django ORM."""
    severity = request.GET.get("severity", "").strip()
    query = request.GET.get("q", "").strip()

    errors = []
    if severity or query:
        qs = Error.objects.select_related("status", "developer", "user")
        if severity:
            qs = qs.filter(severity=severity)
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        errors = qs.order_by("id")

    return render(
        request,
        "errors/error_search.html",
        {
            "errors": errors,
            "severity": severity,
            "query": query,
        },
    )


def statistics(request):
    """Аналитическая страница со статистикой через annotate() и Count()."""
    status_stats = (
        Status.objects
        .annotate(errors_count=Count("errors"))
        .order_by("id")
    )
    dev_stats = (
        Developer.objects
        .annotate(errors_count=Count("errors"))
        .order_by("-errors_count")
    )
    busy_devs = (
        Developer.objects
        .annotate(errors_count=Count("errors"))
        .filter(errors_count__gt=1)
        .order_by("-errors_count")
    )

    return render(
        request,
        "errors/statistics.html",
        {
            "status_stats": status_stats,
            "dev_stats": dev_stats,
            "busy_devs": busy_devs,
        },
    )
