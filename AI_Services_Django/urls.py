"""
Purpose:
    Central URL map for the whole project.

Connects with:
    - recruitment public/internal endpoints
    - recruitment DRF routers (candidates + resumes)
    - JWT token endpoints from simplejwt
    - Django admin
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from recruitment.views import test_redis_cache
from rest_framework.routers import DefaultRouter
from recruitment.views import ResumeViewSet

# DRF router for Resume CRUD APIs.
router = DefaultRouter()
router.register(r"resumes", ResumeViewSet, basename="resume")



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
    # Duplicate include for drf_urls kept from current project wiring.
    path("", include("recruitment.drf_urls")),
] + router.urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



