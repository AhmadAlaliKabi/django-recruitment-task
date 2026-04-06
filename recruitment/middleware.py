"""
Purpose:
    Middleware that logs who accessed resume endpoints.

Connects with:
    - settings.py MIDDLEWARE list
    - request/response cycle for all incoming API requests
"""

import logging


logger = logging.getLogger(__name__)


class ResumeAccessLogMiddleware:
    """
    Log user id and client IP when a resume API endpoint is called.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if "/resumes/" in path:
            user_id = request.user.id if request.user.is_authenticated else None
            ip_address = request.META.get("REMOTE_ADDR", "unknown")
            logger.info("Resume API accessed. user_id=%s ip=%s path=%s", user_id, ip_address, path)

        return self.get_response(request)
