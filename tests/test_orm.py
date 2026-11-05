"""Тесты моделей Django ORM и операций с данными (ПР9)."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freim_project.settings")
django.setup()

from django.core.paginator import Paginator  # noqa: E402
from django.db.models import Count  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from bugtracker.models import Developer, Error, Status, User  # noqa: E402


@pytest.fixture
def client():
    return Client()


def test_orm_models_exist():
    assert User.objects.count() >= 3
    assert Developer.objects.count() >= 3
    assert Status.objects.count() >= 4
    assert Error.objects.count() >= 5


def test_orm_relations():
    err = Error.objects.select_related("status", "developer", "user").first()
    assert err is not None
    assert err.user.name != ""
    assert err.developer.name != ""
    assert err.status.name != ""
    # Reverse relations via related_name="errors"
    assert err.developer.errors.count() >= 1
    assert err.status.errors.count() >= 1


def test_orm_crud():
    status = Status.objects.first()
    user = User.objects.first()
    developer = Developer.objects.first()

    # Create
    new_error = Error.objects.create(
        title="Тестовая ошибка ORM",
        description="Описание для проверки CRUD в Django ORM",
        severity="незначительная",
        priority="Низкий",
        status=status,
        user=user,
        developer=developer,
    )
    assert new_error.id is not None

    # Read
    fetched = Error.objects.get(pk=new_error.id)
    assert fetched.title == "Тестовая ошибка ORM"

    # Update
    fetched.title = "Обновленная ошибка ORM"
    fetched.save(update_fields=["title"])
    refetched = Error.objects.get(pk=new_error.id)
    assert refetched.title == "Обновленная ошибка ORM"

    # Delete
    new_id = new_error.id
    new_error.delete()
    assert not Error.objects.filter(pk=new_id).exists()


def test_orm_filtering_and_sorting(client):
    url = reverse("bugtracker:error_list")

    # Filter by severity
    res = client.get(url, {"severity": "критическая"})
    assert res.status_code == 200
    assert "критическая" in res.content.decode("utf-8")

    # Filter by status
    status = Status.objects.filter(name="Новая").first()
    if status:
        res = client.get(url, {"status": str(status.id)})
        assert res.status_code == 200

    # Sort
    res = client.get(url, {"sort": "title"})
    assert res.status_code == 200

    res = client.get(url, {"sort": "-id"})
    assert res.status_code == 200


def test_orm_pagination():
    qs = Error.objects.all()
    paginator = Paginator(qs, 2)
    page1 = paginator.get_page(1)
    assert len(page1.object_list) == 2
    assert page1.has_next()


def test_orm_aggregation():
    stats = Status.objects.annotate(count=Count("errors")).order_by("id")
    assert stats.count() == Status.objects.count()
    for s in stats:
        assert hasattr(s, "count")
