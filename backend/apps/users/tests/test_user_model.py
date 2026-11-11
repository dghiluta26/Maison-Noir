import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_auth_user_model_is_custom_user():
    assert User._meta.label == "users.User"
    assert User._meta.db_table == "users"


def test_create_user_defaults_to_customer_role():
    user = User.objects.create_user(
        email="client@example.com",
        password="S3cure-pass!",
        first_name="Ana",
        last_name="Pop",
    )

    assert user.role == User.Role.CUSTOMER
    assert user.is_customer and not user.is_admin
    assert not user.is_staff and not user.is_superuser


def test_password_is_hashed_not_stored_in_plain_text():
    user = User.objects.create_user(email="hash@example.com", password="S3cure-pass!")

    assert user.password != "S3cure-pass!"
    assert user.check_password("S3cure-pass!")


def test_email_is_login_field_and_username_is_removed():
    assert User.USERNAME_FIELD == "email"
    assert "username" not in {field.name for field in User._meta.get_fields()}


def test_email_is_normalised_to_lowercase():
    user = User.objects.create_user(email="Client@EXAMPLE.com", password="S3cure-pass!")

    assert user.email == "client@example.com"


def test_email_must_be_unique():
    User.objects.create_user(email="dup@example.com", password="S3cure-pass!")

    with pytest.raises(IntegrityError):
        User.objects.create_user(email="dup@example.com", password="S3cure-pass!")


def test_create_user_without_email_is_rejected():
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="S3cure-pass!")


def test_create_superuser_has_admin_role_and_full_access():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="S3cure-pass!",
        first_name="Admin",
        last_name="Maison",
    )

    assert admin.role == User.Role.ADMIN
    assert admin.is_admin
    assert admin.is_staff and admin.is_superuser


def test_superuser_cannot_have_customer_role():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="bad@example.com", password="S3cure-pass!", role=User.Role.CUSTOMER
        )


def test_database_rejects_unknown_role():
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="role@example.com", password="S3cure-pass!", role="manager")
