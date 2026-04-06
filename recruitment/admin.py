"""
Purpose:
    Django admin registrations for recruitment models.

Connects with:
    - models.py definitions
    - /admin UI for manual data inspection/management
"""

from django.contrib import admin
from .models import Organization, JobPosting, Candidate, Resume
from .models import DailyStats

admin.site.register(Organization)
admin.site.register(JobPosting)
admin.site.register(Resume)


@admin.action(description="Move selected candidates to Interview")
def mark_as_interview(modeladmin, request, queryset):
    queryset.update(application_status=Candidate.STATUS_INTERVIEW)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "application_status",
        "priority_score",
        "expected_salary",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("application_status", "created_at")
    actions = [mark_as_interview]

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    # Stats are system-generated, so admin can view but not manually create/delete.
    list_display = ("job_posting", "date", "application_count")
    ordering = ("-date",)
    readonly_fields = ("job_posting", "date", "application_count")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
