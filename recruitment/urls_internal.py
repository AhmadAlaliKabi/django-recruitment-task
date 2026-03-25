from django.urls import path
from .views import InternalJobListView

app_name = "internal"

urlpatterns = [
    path("jobs/", InternalJobListView.as_view(), name="job-list"),
]