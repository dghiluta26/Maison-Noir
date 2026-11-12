"""
Authentication API (contract: docs/api/auth.md).

POST /api/auth/register/   create a customer and log in        -> 201 {access, user} + cookie
POST /api/auth/login/      email + password                    -> 200 {access, user} + cookie
POST /api/auth/refresh/    uses the mn_refresh cookie (rotated) -> 200 {access, user} + new cookie
POST /api/auth/logout/     blacklists the refresh token         -> 204, cookie deleted
GET  /api/auth/me/         Authorization: Bearer <access>       -> 200 user

The refresh token is never put in a JSON body; it only travels in the
httpOnly cookie configured by settings.AUTH_REFRESH_COOKIE.
"""
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

INVALID_CREDENTIALS = "Invalid email or password."
SESSION_EXPIRED = "Session expired. Please log in again."


def _cookie():
    return settings.AUTH_REFRESH_COOKIE


def _set_refresh_cookie(response, refresh):
    cookie = _cookie()
    response.set_cookie(
        cookie["name"],
        str(refresh),
        max_age=int(jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        path=cookie["path"],
        secure=cookie["secure"],
        httponly=True,
        samesite=cookie["samesite"],
    )


def _delete_refresh_cookie(response):
    cookie = _cookie()
    response.delete_cookie(cookie["name"], path=cookie["path"], samesite=cookie["samesite"])


def _session_response(user, response_status=status.HTTP_200_OK):
    """{access, user} body + a fresh refresh token in the httpOnly cookie."""
    refresh = RefreshToken.for_user(user)
    response = Response(
        {"access": str(refresh.access_token), "user": UserSerializer(user).data},
        status=response_status,
    )
    _set_refresh_cookie(response, refresh)
    return response


def _session_expired():
    # Returned directly (not raised): these views have no authentication
    # classes, so a raised AuthenticationFailed would be turned into a 403.
    response = Response({"detail": SESSION_EXPIRED}, status=status.HTTP_401_UNAUTHORIZED)
    _delete_refresh_cookie(response)
    return response


class PublicAuthView(APIView):
    """Auth entry points: open to everyone and ignore any Authorization header."""

    permission_classes = [AllowAny]
    authentication_classes = []


class RegisterView(PublicAuthView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        update_last_login(None, user)
        return _session_response(user, status.HTTP_201_CREATED)


class LoginView(PublicAuthView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user is None:
            # Same message for unknown email, wrong password and inactive account.
            return Response({"detail": INVALID_CREDENTIALS}, status=status.HTTP_401_UNAUTHORIZED)
        update_last_login(None, user)
        return _session_response(user)


class RefreshView(PublicAuthView):
    def post(self, request):
        raw_token = request.COOKIES.get(_cookie()["name"])
        if not raw_token:
            return _session_expired()

        try:
            # Verifies signature and expiry, and rejects blacklisted tokens.
            old_refresh = RefreshToken(raw_token)
        except TokenError:
            return _session_expired()

        user = User.objects.filter(
            pk=old_refresh.get(jwt_settings.USER_ID_CLAIM), is_active=True
        ).first()
        if user is None:
            return _session_expired()

        # Rotation: the old refresh token can never be used again.
        old_refresh.blacklist()
        return _session_response(user)


class LogoutView(PublicAuthView):
    def post(self, request):
        raw_token = request.COOKIES.get(_cookie()["name"])
        if raw_token:
            try:
                RefreshToken(raw_token).blacklist()
            except TokenError:
                pass  # Already invalid; logging out must still succeed.
        response = Response(status=status.HTTP_204_NO_CONTENT)
        _delete_refresh_cookie(response)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
