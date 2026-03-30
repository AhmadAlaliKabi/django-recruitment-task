from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from recruitment.views import test_redis_cache

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/public/", include(("recruitment.urls_public", "public"), namespace="public")),
    path("api/internal/", include(("recruitment.urls_internal", "internal"), namespace="internal")),
    path("api/", include("recruitment.drf_urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("test-cache/", test_redis_cache, name="test_cache"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)