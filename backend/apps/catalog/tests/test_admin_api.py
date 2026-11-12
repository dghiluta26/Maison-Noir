"""
Admin-only endpoints are blocked on the server for regular users (spec A10),
not merely hidden in the interface.
"""
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.catalog.models import Product

User = get_user_model()

pytestmark = pytest.mark.django_db

PASSWORD = "Parfum-de-nuit-26"


@pytest.fixture(autouse=True)
def catalogue():
    call_command("seed_catalogue", stdout=StringIO())
    Product.objects.filter(sku="MN-AH-P").update(is_active=False)


@pytest.fixture
def customer():
    return User.objects.create_user(email="ana@example.com", password=PASSWORD, first_name="Ana", last_name="Pop")


@pytest.fixture
def admin():
    return User.objects.create_superuser(email="admin@example.com", password=PASSWORD, first_name="Admin", last_name="Maison")


def client_for(user=None):
    client = APIClient()
    if user is not None:
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user).access_token}")
    return client


# --- Access control ------------------------------------------------------


@pytest.mark.parametrize("url", ["/api/admin/products/", "/api/admin/products/after-hours-eau-de-parfum/"])
def test_visitor_gets_401(url):
    response = client_for().get(url)

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication credentials were not provided."}


@pytest.mark.parametrize("url", ["/api/admin/products/", "/api/admin/products/after-hours-eau-de-parfum/"])
def test_customer_gets_403(customer, url):
    response = client_for(customer).get(url)

    assert response.status_code == 403
    assert response.json() == {"detail": "You do not have permission to perform this action."}


def test_customer_with_staff_flag_but_customer_role_is_still_blocked(customer):
    # Access is decided by the role, not by Django's is_staff flag.
    customer.is_staff = True
    customer.save()

    assert client_for(customer).get("/api/admin/products/").status_code == 403


def test_invalid_token_gets_401():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")

    assert client.get("/api/admin/products/").status_code == 401


# --- Admin behaviour -----------------------------------------------------


def test_admin_sees_all_products_including_inactive(admin):
    body = client_for(admin).get("/api/admin/products/").json()

    assert body["count"] == 32
    inactive = [p for p in body["results"] if p["sku"] == "MN-AH-P"]
    assert inactive and inactive[0]["is_active"] is False
    assert {"is_active", "created_at", "updated_at", "description", "images"} <= set(body["results"][0])


def test_public_catalogue_still_hides_inactive_product():
    assert APIClient().get("/api/products/").json()["count"] == 31


def test_admin_can_filter_by_active_flag(admin):
    client = client_for(admin)

    assert client.get("/api/admin/products/?is_active=false").json()["count"] == 1
    assert client.get("/api/admin/products/?is_active=true").json()["count"] == 31


def test_admin_can_open_inactive_product(admin):
    response = client_for(admin).get("/api/admin/products/after-hours-eau-de-parfum/")

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_admin_api_is_read_only_for_now(admin):
    client = client_for(admin)

    assert client.post("/api/admin/products/", {}, format="json").status_code == 405
    assert client.delete("/api/admin/products/after-hours-eau-de-parfum/").status_code == 405


# --- Django admin site ---------------------------------------------------


def test_customer_cannot_open_django_admin(client, customer):
    client.force_login(customer)

    response = client.get("/admin/")

    assert response.status_code == 302
    assert response.url.startswith("/admin/login/")


def test_admin_can_open_django_admin(client, admin):
    client.force_login(admin)

    assert client.get("/admin/").status_code == 200
