"""
Purpose:
    Background jobs for heavy/periodic work:
    1) Parse resume PDFs and extract skills.
    2) Generate daily application stats.

Connects with:
    - models.py (Resume, JobPosting, DailyStats)
    - serializers.py (resume creation triggers parse task)
    - celery.py/settings.py (task registration + scheduling)
"""

import re
from celery import shared_task
from pypdf import PdfReader
from recruitment.models import JobPosting, Resume, DailyStats
from django.utils import timezone



def extract_text_from_pdf(file_path):
    # Reads all pages and concatenates text for later parsing.
    text = ""

    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")

    return text.strip()


def parse_candidate_text(text):
    # Lightweight regex parser (not true AI yet) for simple labeled resume text.
    name_match = re.search(r"name:\s*(.+)", text, re.IGNORECASE)
    email_match = re.search(r"email:\s*([^\s]+)", text, re.IGNORECASE)
    phone_match = re.search(r"phone:\s*(.+)", text, re.IGNORECASE)
    skills_match = re.search(r"skills:\s*(.+)", text, re.IGNORECASE)

    name = name_match.group(1).strip() if name_match else None
    email = email_match.group(1).strip() if email_match else None
    phone = phone_match.group(1).strip() if phone_match else None

    skills = []
    if skills_match:
        skills = [skill.strip() for skill in skills_match.group(1).split(",") if skill.strip()]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
    }
@shared_task
def generate_daily_stats():
    # For each job, store/update "how many resumes applied" for today.
    today = timezone.now().date()

    for job in JobPosting.objects.all():
        application_count = Resume.objects.filter(
            job_posting=job,
            uploaded_at__date=today
        ).count()

        DailyStats.objects.update_or_create(
            job_posting=job,
            date=today,
            defaults={"application_count": application_count}
        )

    return f"Daily stats generated for {today}"

@shared_task
def parse_resume_task(resume_id):
    # Background processing after upload so API stays fast.
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return "Resume not found"

    file_path = resume.file.path

    extracted_text = extract_text_from_pdf(file_path)
    parsed_data = parse_candidate_text(extracted_text)

    resume.extracted_text = extracted_text
    resume.ai_extracted_skills = parsed_data.get("skills", [])
    resume.save()

    return parsed_data

