"""
Purpose:
    Data models for the recruitment domain (orgs, jobs, candidates, resumes, stats).

Connects with:
    - serializers.py for API IO
    - views.py for read/write operations
    - admin.py for admin management
    - tasks.py for async resume parsing and daily stats
    - migrations/ for DB schema history
"""

from django.db import models

class DailyStats(models.Model):
    # One row per job per day, storing number of applications.
    job_posting = models.ForeignKey('JobPosting', on_delete=models.CASCADE)
    date = models.DateField()
    application_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('job_posting', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.job_posting} - {self.date} - {self.application_count}"

class Organization(models.Model):
    # Hiring company/organization that owns job postings.
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    # A single job ad published by one organization.
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="job_postings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.organization.name}"


class Candidate(models.Model):
    # Applicant profile, shared across multiple resumes if needed.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Resume(models.Model):
    # Uploaded resume file + extracted AI text/skills.
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="resumes"
    )
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resumes"
    )
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    ai_extracted_skills = models.JSONField(default=list, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"Resume for {self.candidate}"

    file = models.FileField(upload_to="resumes/")
