from django.contrib import admin
from .models import Organization, JobPosting, Candidate, Resume
from .models import DailyStats

admin.site.register(Organization)
admin.site.register(JobPosting)
admin.site.register(Candidate)
admin.site.register(Resume)

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ("job_posting", "date", "application_count")
    ordering = ("-date",)
    readonly_fields = ("job_posting", "date", "application_count")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False