"""
Purpose:
    DRF router URLs for authenticated API endpoints.

Connects with:
    - views.py (CandidateViewSet, ResumeViewSet)
    - project urls.py under /api/
"""

from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, ResumeViewSet

router = DefaultRouter()
router.register(r"candidates", CandidateViewSet, basename="candidate")
router.register(r"resumes", ResumeViewSet, basename="resume")

urlpatterns = router.urls
