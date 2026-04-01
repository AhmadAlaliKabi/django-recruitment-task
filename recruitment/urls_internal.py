"""
Purpose:
    Internal URL routes for job listing with internal details.

Connects with:
    - views.py (InternalJobListView)
    - project urls.py under /api/internal/
"""

from django.urls import path
from .views import InternalJobListView

app_name = "internal"

urlpatterns = [
    path("jobs/", InternalJobListView.as_view(), name="job-list"),
]
