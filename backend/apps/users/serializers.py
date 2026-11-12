"""Serializers for the authentication API (contract: docs/api/auth.md)."""
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User object returned by register, login, refresh and me."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "role"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Creates a CUSTOMER account. `role` is not a field here, so a `role` sent
    by the client is ignored and nobody can register as admin.
    """

    # Declared explicitly to replace the model's default unique validator
    # with a case-insensitive check and a clearer message.
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(write_only=True, trim_whitespace=False, style={"input_type": "password"})
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone_number"]

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return email

    def validate(self, attrs):
        # Run Django's password validators against the would-be user, so the
        # "too similar to your email/name" check can work.
        candidate = User(
            email=attrs.get("email", ""),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )
        try:
            password_validation.validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": list(error.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, style={"input_type": "password"})

    def validate(self, attrs):
        """Sets attrs["user"], or None when the credentials are wrong or the account is inactive."""
        attrs["user"] = authenticate(
            request=self.context.get("request"),
            email=attrs["email"].strip().lower(),
            password=attrs["password"],
        )
        return attrs
