from django.contrib import admin
from .models import Organization, JobPosting, Candidate, Resume


@admin.action(description="Move selected candidates to Interview")
def move_to_interview(modeladmin, request, queryset):
    queryset.update(application_status='interview')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'application_status',
        #'priority_score',
        'created_at',
    )
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('application_status', 'created_at')
    actions = [move_to_interview]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'website', 'created_at')
    search_fields = ('name', 'industry')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'location', 'is_active', 'posted_at')
    search_fields = ('title', 'organization__name')
    list_filter = ('is_active', 'location', 'posted_at')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_posting', 'file_name', 'uploaded_at')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'file_name')
    list_filter = ('uploaded_at',)