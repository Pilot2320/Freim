"""Тесты админ-панели Django и расширенных возможностей ORM (ПР10)."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freim_project.settings")
django.setup()

from django.contrib.admin.sites import AdminSite  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from django.contrib.messages.storage.fallback import (  # noqa: E402
    FallbackStorage,
)
from django.contrib.sessions.backends.db import (  # noqa: E402
    SessionStore,
)
from django.test import Client, RequestFactory  # noqa: E402
from django.urls import reverse  # noqa: E402

from bugtracker.admin import (  # noqa: E402
    DeveloperAdmin,
    ErrorAdmin,
    ErrorInline,
    StatusAdmin,
    UserAdmin,
)
from bugtracker.context_processors import (  # noqa: E402
    bugtracker_context,
)
from bugtracker.models import (  # noqa: E402
    Developer,
    Error,
    Priority,
    Severity,
    Status,
    User,
)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_client():
    auth_user_model = get_user_model()
    admin_user, _ = auth_user_model.objects.get_or_create(
        username="admin_test",
        defaults={
            "email": "adm_test@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin_user.set_password("admin_pass")
    admin_user.save()

    c = Client()
    c.force_login(admin_user)
    return c


def test_admin_models_registered():
    from django.contrib import admin

    assert Error in admin.site._registry
    assert Developer in admin.site._registry
    assert User in admin.site._registry
    assert Status in admin.site._registry


def test_error_admin_configuration():
    site = AdminSite()
    error_admin = ErrorAdmin(Error, site)

    assert "id" in error_admin.list_display
    assert "title" in error_admin.list_display
    assert "severity" in error_admin.list_display
    assert "priority" in error_admin.list_display
    assert "status" in error_admin.list_display

    assert ("id", "title") == error_admin.list_display_links
    assert "title" in error_admin.search_fields
    assert "developer__name" in error_admin.search_fields

    assert "severity" in error_admin.list_filter
    assert "status" in error_admin.list_filter
    assert "priority" in error_admin.list_editable
    assert "id" in error_admin.readonly_fields


def test_developer_and_user_admin_inlines():
    site = AdminSite()
    dev_admin = DeveloperAdmin(Developer, site)
    user_admin = UserAdmin(User, site)
    status_admin = StatusAdmin(Status, site)

    assert ErrorInline in dev_admin.inlines
    assert ErrorInline in user_admin.inlines

    # Custom column errors_count
    dev = Developer.objects.first()
    if dev:
        assert isinstance(dev_admin.errors_count(dev), int)

    usr = User.objects.first()
    if usr:
        assert isinstance(user_admin.errors_count(usr), int)

    st = Status.objects.first()
    if st:
        assert isinstance(status_admin.errors_count(st), int)


def test_admin_actions():
    site = AdminSite()
    error_admin = ErrorAdmin(Error, site)

    dev = Developer.objects.first()
    usr = User.objects.first()
    st_new = Status.objects.filter(name="Новая").first()

    err = Error.objects.create(
        title="Действие админки",
        description="Проверка actions",
        severity=Severity.MINOR,
        priority=Priority.LOW,
        status=st_new,
        user=usr,
        developer=dev,
    )

    rf = RequestFactory()
    request = rf.post("/")
    request.user = usr
    request.session = SessionStore()
    request._messages = FallbackStorage(request)

    # Action 1: make_high_priority
    qs = Error.objects.filter(pk=err.id)
    error_admin.make_high_priority(request, qs)
    err.refresh_from_db()
    assert err.priority == Priority.HIGH

    # Action 2: mark_closed
    error_admin.mark_closed(request, qs)
    err.refresh_from_db()
    assert err.status.name == "Закрыта"

    err.delete()


def test_admin_views_accessible(admin_client):
    urls = [
        reverse("admin:index"),
        reverse("admin:bugtracker_error_changelist"),
        reverse("admin:bugtracker_developer_changelist"),
        reverse("admin:bugtracker_user_changelist"),
        reverse("admin:bugtracker_status_changelist"),
        reverse("admin:bugtracker_error_add"),
    ]
    for url in urls:
        resp = admin_client.get(url)
        assert resp.status_code == 200


def test_context_processor():
    rf = RequestFactory()
    request = rf.get("/")
    data = bugtracker_context(request)

    assert "site_name" in data
    assert data["site_name"] == "Freim"
    assert "total_errors_count" in data
    assert data["total_errors_count"] >= 5
    assert "active_errors_count" in data


def test_custom_queryset_and_manager():
    total_count = Error.objects.count()
    active_errors = Error.objects.active()
    assert active_errors.count() <= total_count

    critical_errors = Error.objects.critical()
    for err in critical_errors:
        assert err.severity == Severity.CRITICAL

    high_errors = Error.objects.high_priority()
    for err in high_errors:
        assert err.priority == Priority.HIGH

    by_status = Error.objects.by_status("Новая")
    for err in by_status:
        assert err.status.name == "Новая"


def test_error_close_method():
    dev = Developer.objects.first()
    usr = User.objects.first()
    st_new = Status.objects.filter(name="Новая").first()

    err = Error.objects.create(
        title="Тест метода close",
        description="Проверка close()",
        severity=Severity.MINOR,
        priority=Priority.LOW,
        status=st_new,
        user=usr,
        developer=dev,
    )
    err.close()
    err.refresh_from_db()
    assert err.status.name == "Закрыта"
    err.delete()
