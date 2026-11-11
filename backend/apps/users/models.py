"""
User model.

Implements the CUSTOMERS entity of the MAISON NOIR E-R model
(customer_id, first_name, last_name, email, phone_number) as Django's
authentication user, extended with a `role` so that customers and
administrators share one login table.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        ADMIN = "admin", "Admin"

    # Email is the login identifier; Django's default username is removed.
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    phone_number = models.CharField("phone number", max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = "email"
    # Asked by `createsuperuser` in addition to email and password.
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(role__in=["customer", "admin"]),
                name="users_role_valid",
            ),
        ]

    def __str__(self):
        return self.email

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN

    @property
    def is_customer(self) -> bool:
        return self.role == self.Role.CUSTOMER
