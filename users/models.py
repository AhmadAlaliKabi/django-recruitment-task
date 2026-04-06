"""
Purpose:
    Custom User model for authentication with email instead of username.

Connects with:
    - settings.py AUTH_USER_MODEL
    - users.managers.UserManager
    - JWT/authentication flow
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Beginner-friendly custom user model:
    - uses email as the username field
    - still keeps first_name / last_name from AbstractUser
    """

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
