"""Central URL map for admin, JWT auth, and recruitment APIs."""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from recruitment.views import test_redis_cache



urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Public + internal plain Django views
    path("api/public/", include(("recruitment.urls_public", "public"), namespace="public")),
    path("api/internal/", include(("recruitment.urls_internal", "internal"), namespace="internal")),

    # DRF candidates routes from recruitment.drf_urls
    path("api/", include("recruitment.drf_urls")),

    # Auth token endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Simple Redis sanity endpoint
    path("test-cache/", test_redis_cache, name="test_cache"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



