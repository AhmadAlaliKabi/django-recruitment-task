import logging

logger = logging.getLogger(__name__)


class ResumeAccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path.lower()
        if "/admin/recruitment/resume/" in path:
            user_id = request.user.id if request.user.is_authenticated else None
            ip_address = self.get_client_ip(request)

            logger.info(
                f"Resume access detected | user_id={user_id} | ip_address={ip_address} | path={request.path}"
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")