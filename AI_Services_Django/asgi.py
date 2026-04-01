"""
Purpose:
    ASGI entrypoint (used if you run async servers like uvicorn/daphne).

Connects with:
    - AI_Services_Django.settings
    - Deployment layer that serves this app over ASGI
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AI_Services_Django.settings')

application = get_asgi_application()
