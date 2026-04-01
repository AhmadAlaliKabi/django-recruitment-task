"""
Purpose:
    DRF router URLs for recruitment viewsets used under /api/.

Connects with:
    - views.py CandidateViewSet
    - project urls.py include("recruitment.drf_urls")
"""

from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = router.urls
