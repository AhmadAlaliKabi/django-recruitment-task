"""
Purpose:
    WSGI entrypoint (used by classic Django servers like gunicorn/uwsgi).

Connects with:
    - AI_Services_Django.settings
    - Deployment layer that serves this app over WSGI
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AI_Services_Django.settings')

application = get_wsgi_application()
