"""
Purpose:
    Django app configuration for the custom users app.

Connects with:
    - settings.py INSTALLED_APPS
    - users model registration in Django app registry
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
