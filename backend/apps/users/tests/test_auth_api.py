"""Authentication API tests — one block per endpoint of docs/api/auth.md."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.permissions import IsAdminRole

User = get_user_model()

pytestmark = pytest.mark.django_db

COOKIE = "mn_refresh"
PASSWORD = "Parfum-de-nuit-26"
USER_FIELDS = {"id", "email", "first_name", "last_name", "phone_number", "role"}


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def customer():
    return User.objects.create_user(
        email="ana.pop@example.com", password=PASSWORD, first_name="Ana", last_name="Pop"
    )


@pytest.fixture
def admin():
    return User.objects.create_superuser(
        email="admin@example.com", password=PASSWORD, first_name="Admin", last_name="Maison"
    )


def register_payload(**overrides):
    data = {
        "email": "claire.martin@example.com",
        "password": PASSWORD,
        "first_name": "Claire",
        "last_name": "Martin",
        "phone_number": "+40712345678",
    }
    data.update(overrides)
    return data


def login(api, email="ana.pop@example.com", password=PASSWORD):
    return api.post("/api/auth/login/", {"email": email, "password": password}, format="json")


def assert_refresh_cookie(response):
    cookie = response.cookies[COOKIE]
    assert cookie.value
    assert cookie["httponly"] is True
    assert cookie["path"] == "/api/auth/"
    assert cookie["samesite"] == "Lax"
    assert int(cookie["max-age"]) == 7 * 24 * 3600


# --- Register ------------------------------------------------------------


def test_register_creates_customer_and_logs_in(api):
    response = api.post("/api/auth/register/", register_payload(), format="json")

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"access", "user"}
    assert set(body["user"]) == USER_FIELDS
    assert body["user"]["role"] == "customer"
    assert body["user"]["phone_number"] == "+40712345678"
    assert "refresh" not in body  # refresh token only travels in the cookie
    assert_refresh_cookie(response)


def test_register_hashes_password_and_lowercases_email(api):
    api.post("/api/auth/register/", register_payload(email="Claire.MARTIN@Example.com"), format="json")

    user = User.objects.get()
    assert user.email == "claire.martin@example.com"
    assert user.password != PASSWORD
    assert user.check_password(PASSWORD)


def test_register_ignores_role_from_client(api):
    response = api.post("/api/auth/register/", register_payload(role="admin"), format="json")

    assert response.json()["user"]["role"] == "customer"
    assert User.objects.get().is_staff is False


def test_register_phone_is_optional(api):
    payload = register_payload()
    del payload["phone_number"]

    response = api.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 201
    assert response.json()["user"]["phone_number"] == ""


def test_register_rejects_duplicate_email_case_insensitively(api, customer):
    response = api.post("/api/auth/register/", register_payload(email="ANA.POP@example.com"), format="json")

    assert response.status_code == 400
    assert response.json() == {"email": ["An account with this email already exists."]}


@pytest.mark.parametrize(
    "password, expected",
    [
        ("Short1!", "This password is too short. It must contain at least 8 characters."),
        ("1234567890", "This password is entirely numeric."),
        ("password123", "This password is too common."),
        # Similarity is checked against the new user's email/name (threshold 0.7).
        ("claire.martin@exa", "The password is too similar to the email address."),
    ],
)
def test_register_applies_django_password_validators(api, password, expected):
    response = api.post("/api/auth/register/", register_payload(password=password), format="json")

    assert response.status_code == 400
    assert expected in response.json()["password"]


def test_register_reports_missing_fields(api):
    response = api.post("/api/auth/register/", {}, format="json")

    assert response.status_code == 400
    assert set(response.json()) == {"email", "password", "first_name", "last_name"}
    assert User.objects.count() == 0


def test_register_access_token_works_for_me(api):
    access = api.post("/api/auth/register/", register_payload(), format="json").json()["access"]

    api.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = api.get("/api/auth/me/")

    assert response.status_code == 200
    assert response.json()["email"] == "claire.martin@example.com"


# --- Login ---------------------------------------------------------------


def test_login_success_returns_access_user_and_cookie(api, customer):
    response = login(api)

    assert response.status_code == 200
    assert set(response.json()) == {"access", "user"}
    assert response.json()["user"]["email"] == "ana.pop@example.com"
    assert_refresh_cookie(response)
    customer.refresh_from_db()
    assert customer.last_login is not None


def test_login_email_is_case_insensitive(api, customer):
    assert login(api, email="  Ana.Pop@EXAMPLE.com ").status_code == 200


@pytest.mark.parametrize(
    "email, password",
    [("ana.pop@example.com", "wrong-password"), ("nobody@example.com", PASSWORD)],
)
def test_login_failure_gives_same_401_message(api, customer, email, password):
    response = login(api, email=email, password=password)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}
    assert COOKIE not in response.cookies


def test_login_rejects_inactive_account(api, customer):
    customer.is_active = False
    customer.save()

    response = login(api)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}


def test_login_reports_missing_fields(api):
    response = api.post("/api/auth/login/", {}, format="json")

    assert response.status_code == 400
    assert set(response.json()) == {"email", "password"}


def test_login_ignores_invalid_bearer_header(api, customer):
    api.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")

    assert login(api).status_code == 200


# --- Refresh -------------------------------------------------------------


def test_refresh_with_cookie_returns_new_access_and_rotates_cookie(api, customer):
    login_response = login(api)
    old_cookie = login_response.cookies[COOKIE].value

    response = api.post("/api/auth/refresh/")

    assert response.status_code == 200
    assert set(response.json()) == {"access", "user"}
    assert response.json()["user"]["email"] == "ana.pop@example.com"
    assert_refresh_cookie(response)
    assert response.cookies[COOKIE].value != old_cookie


def test_refresh_token_cannot_be_reused_after_rotation(api, customer):
    old_cookie = login(api).cookies[COOKIE].value
    api.post("/api/auth/refresh/")  # rotates; the old token is blacklisted

    attacker = APIClient()
    attacker.cookies[COOKIE] = old_cookie
    response = attacker.post("/api/auth/refresh/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Session expired. Please log in again."}


def test_refresh_without_cookie_returns_401(api):
    response = api.post("/api/auth/refresh/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Session expired. Please log in again."}


def test_refresh_with_garbage_cookie_returns_401_and_clears_it(api):
    api.cookies[COOKIE] = "garbage"

    response = api.post("/api/auth/refresh/")

    assert response.status_code == 401
    assert response.cookies[COOKIE].value == ""


def test_refresh_rejects_deactivated_user(api, customer):
    login(api)
    customer.is_active = False
    customer.save()

    assert api.post("/api/auth/refresh/").status_code == 401


# --- Logout --------------------------------------------------------------


def test_logout_blacklists_refresh_token_and_deletes_cookie(api, customer):
    token = login(api).cookies[COOKIE].value

    response = api.post("/api/auth/logout/")

    assert response.status_code == 204
    assert response.cookies[COOKIE].value == ""
    assert int(response.cookies[COOKIE]["max-age"]) == 0

    replay = APIClient()
    replay.cookies[COOKIE] = token
    assert replay.post("/api/auth/refresh/").status_code == 401


def test_logout_without_session_still_returns_204(api):
    assert api.post("/api/auth/logout/").status_code == 204


def test_logout_with_invalid_cookie_still_returns_204(api):
    api.cookies[COOKIE] = "garbage"

    assert api.post("/api/auth/logout/").status_code == 204


# --- Me ------------------------------------------------------------------


def test_me_returns_current_user(api, customer):
    access = login(api).json()["access"]
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = api.get("/api/auth/me/")

    assert response.status_code == 200
    assert set(response.json()) == USER_FIELDS
    assert response.json()["role"] == "customer"


def test_me_without_token_returns_401(api):
    response = api.get("/api/auth/me/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication credentials were not provided."}


def test_me_with_invalid_token_returns_401(api):
    api.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")

    assert api.get("/api/auth/me/").status_code == 401


def test_refresh_token_is_not_accepted_as_access_token(api, customer):
    refresh = str(RefreshToken.for_user(customer))
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh}")

    assert api.get("/api/auth/me/").status_code == 401


# --- Public catalogue ----------------------------------------------------


def test_catalogue_stays_public_even_with_expired_or_bad_token(api):
    api.credentials(HTTP_AUTHORIZATION="Bearer expired-or-garbage")

    assert api.get("/api/products/").status_code == 200
    assert api.get("/api/categories/").status_code == 200


# --- Roles: IsAdminRole --------------------------------------------------


class AdminOnlyView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({"ok": True})


def call_admin_only(user=None):
    request = APIRequestFactory().get("/admin-only/")
    if user is not None:
        access = str(RefreshToken.for_user(user).access_token)
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access}"
    return AdminOnlyView.as_view()(request)


def test_admin_only_endpoint_rejects_visitor_with_401():
    assert call_admin_only().status_code == 401


def test_admin_only_endpoint_rejects_customer_with_403(customer):
    response = call_admin_only(customer)

    assert response.status_code == 403
    assert response.data == {"detail": "You do not have permission to perform this action."}


def test_admin_only_endpoint_allows_admin(admin):
    assert call_admin_only(admin).status_code == 200
