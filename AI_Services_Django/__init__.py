"""
Purpose:
    Package init for the project and Celery exposure.

Connects with:
    - celery.py so `celery_app` is loaded when Django starts.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
