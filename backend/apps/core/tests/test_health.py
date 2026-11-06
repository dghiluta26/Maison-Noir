from unittest import mock

import pytest
from django.db import OperationalError
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_health_returns_ok_when_database_is_reachable(api_client):
    response = api_client.get(reverse("core:health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_returns_503_when_database_is_unavailable(api_client):
    with mock.patch(
        "apps.core.views.connection.cursor",
        side_effect=OperationalError("connection refused"),
    ):
        response = api_client.get(reverse("core:health"))

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "unavailable"}


def test_health_rejects_write_methods(api_client):
    response = api_client.post(reverse("core:health"))

    assert response.status_code == 405
