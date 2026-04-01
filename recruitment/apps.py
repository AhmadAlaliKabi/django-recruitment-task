"""
Purpose:
    Django app configuration for the recruitment app.

Connects with:
    - settings.py INSTALLED_APPS entry ('recruitment')
"""

from django.apps import AppConfig


class RecruitmentConfig(AppConfig):
    name = 'recruitment'
