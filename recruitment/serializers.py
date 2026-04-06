from rest_framework import serializers

from .models import Candidate, Resume
from .permissions import IsDepartmentHead
from .tasks import parse_resume_task


class CandidateSerializer(serializers.ModelSerializer):
    """
    Candidate serializer.
    Expected salary is hidden unless the user passes IsDepartmentHead.
    """

    class Meta:
        model = Candidate
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        permission = IsDepartmentHead()
        can_view_salary = bool(request and permission.has_permission(request, self.context.get("view")))
        if not can_view_salary:
            data.pop("expected_salary", None)
        return data


class ResumeSerializer(serializers.ModelSerializer):
    """
    Resume serializer with file upload support.
    After saving, it triggers a Celery task to parse the PDF.
    """

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
            "expected_salary",
        ]
        read_only_fields = ["uploaded_at", "extracted_text", "ai_extracted_skills"]
        extra_kwargs = {
            "file_name": {"required": False, "allow_blank": True},
            "job_posting": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        # If file_name is missing, use the uploaded file's name.
        uploaded_file = validated_data.get("file")
        if uploaded_file and not validated_data.get("file_name"):
            validated_data["file_name"] = uploaded_file.name

        resume = Resume.objects.create(**validated_data)
        parse_resume_task.delay(resume.id)
        return resume


class SalaryPredictionInputSerializer(serializers.Serializer):
    """
    Input validation for salary prediction endpoint.
    Matches training feature names and expected types.
    """

    Department = serializers.CharField(max_length=100)
    Experience_Years = serializers.IntegerField(min_value=0)
    Education_Level = serializers.CharField(max_length=100)
    Age = serializers.IntegerField(min_value=16, max_value=100)
    Gender = serializers.CharField(max_length=20)
    City = serializers.CharField(max_length=100)
