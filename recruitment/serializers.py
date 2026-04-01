# recruitment/serializers.py
"""
Purpose:
    DRF serializers that validate/transform Candidate and Resume data for APIs.

Connects with:
    - models.py for DB writes/reads
    - views.py viewsets
    - tasks.py via Celery trigger after resume creation
"""

from rest_framework import serializers
from .models import Candidate, Resume
from .tasks import parse_resume_task


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "candidate",
            "job_posting",
            "file",
            "file_name",
            "uploaded_at",
            "extracted_text",
            "ai_extracted_skills",
        ]
        read_only_fields = ["uploaded_at", "extracted_text", "ai_extracted_skills"]
        extra_kwargs = {
            "file_name": {"required": False, "allow_blank": True},
            "job_posting": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        # If client did not pass file_name manually, derive it from uploaded file.
        uploaded_file = validated_data.get("file")

        if uploaded_file and not validated_data.get("file_name"):
            validated_data["file_name"] = uploaded_file.name

        # Save DB row first, then run async parser in background.
        resume = Resume.objects.create(**validated_data)

        print("Sending task to Celery for resume:", resume.id)
        parse_resume_task.delay(resume.id)

        return resume
