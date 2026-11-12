"""
Spec A4: passwords must be stored with bcrypt or Argon2.

The test settings use a fast hasher, so these tests switch back to the real
project hashers from config.settings.base.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import override_settings
from rest_framework.test import APIClient

from config.settings import base

User = get_user_model()

pytestmark = pytest.mark.django_db

PASSWORD = "Parfum-de-nuit-26"
project_hashers = override_settings(PASSWORD_HASHERS=base.PASSWORD_HASHERS)


def test_project_uses_argon2_as_default_hasher():
    assert base.PASSWORD_HASHERS[0] == "django.contrib.auth.hashers.Argon2PasswordHasher"


@project_hashers
def test_registered_password_is_stored_with_argon2():
    APIClient().post(
        "/api/auth/register/",
        {"email": "ana@example.com", "password": PASSWORD, "first_name": "Ana", "last_name": "Pop"},
        format="json",
    )

    stored = User.objects.get(email="ana@example.com").password
    assert stored.startswith("argon2$")
    assert PASSWORD not in stored


@project_hashers
def test_old_pbkdf2_password_is_upgraded_to_argon2_on_login():
    user = User.objects.create(
        email="old@example.com",
        first_name="Old",
        last_name="Account",
        password=make_password(PASSWORD, hasher="pbkdf2_sha256"),
    )
    assert user.password.startswith("pbkdf2_sha256$")

    response = APIClient().post(
        "/api/auth/login/", {"email": "old@example.com", "password": PASSWORD}, format="json"
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.password.startswith("argon2$")
