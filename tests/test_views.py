import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freim_project.settings")
django.setup()

from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402


@pytest.fixture
def client():
    return Client()


def test_homepage_view(client):
    url = reverse("homepage:index")
    response = client.get(url)
    assert response.status_code == 200
    assert "Freim" in response.content.decode("utf-8")


def test_error_list_view(client):
    url = reverse("bugtracker:error_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Список ошибок" in response.content.decode("utf-8")


def test_error_detail_found(client):
    url = reverse("bugtracker:error_detail", kwargs={"error_id": 1})
    response = client.get(url)
    assert response.status_code == 200
    assert "Описание" in response.content.decode("utf-8")


def test_error_detail_not_found(client):
    url = reverse("bugtracker:error_detail", kwargs={"error_id": 9999})
    response = client.get(url)
    assert response.status_code == 404
    assert "Ошибка не найдена" in response.content.decode("utf-8")
