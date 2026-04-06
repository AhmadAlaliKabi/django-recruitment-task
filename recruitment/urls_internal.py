"""
Purpose:
    Internal URL routes for protected internal APIs.

Connects with:
    - views.py (InternalJobListView, SalaryPredictionView)
    - project urls.py under /api/internal/
"""

from django.urls import path
from .views import InternalJobListView, SalaryPredictionView

app_name = "internal"

urlpatterns = [
    path("jobs/", InternalJobListView.as_view(), name="job-list"),
    path("predict-salary/", SalaryPredictionView.as_view(), name="predict-salary"),
]
