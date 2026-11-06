"""Settings used by pytest. Tests run against a temporary PostgreSQL test database."""
from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost"]

# Fast password hashing for tests only. Never use this in other environments.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
