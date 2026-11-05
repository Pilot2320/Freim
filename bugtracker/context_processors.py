"""Контекстные процессоры приложения bugtracker (ПР10)."""

from .models import Error


def bugtracker_context(request):
    """Передаёт общие показатели системы в шаблоны Freim."""
    return {
        "site_name": "Freim",
        "total_errors_count": Error.objects.count(),
        "active_errors_count": Error.objects.active().count(),
        "critical_errors_count": Error.objects.critical().count(),
    }

