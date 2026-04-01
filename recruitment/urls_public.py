"""
Purpose:
    Public-facing URL routes (no JWT needed) for browsing jobs/applying.

Connects with:
    - views.py (PublicJobListView, JobApplicationView)
    - project urls.py under /api/public/
"""

from django.urls import path
from .views import PublicJobListView, JobApplicationView

app_name = "public"

urlpatterns = [
    path("jobs/", PublicJobListView.as_view(), name="job-list"),
    path("apply/", JobApplicationView.as_view(), name="job-apply"),
]
