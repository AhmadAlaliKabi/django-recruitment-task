from django.urls import path
from .views import PublicJobListView, JobApplicationView

app_name = "public"

urlpatterns = [
    path("jobs/", PublicJobListView.as_view(), name="job-list"),
    path("apply/", JobApplicationView.as_view(), name="job-apply"),
]