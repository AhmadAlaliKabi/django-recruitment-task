"""
Purpose:
    Celery app bootstrap so worker/beat processes can load Django settings and tasks.

Connects with:
    - settings.py (CELERY_* config)
    - recruitment.tasks (auto-discovered shared tasks)
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AI_Services_Django.settings')

app = Celery('AI_Services_Django')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
