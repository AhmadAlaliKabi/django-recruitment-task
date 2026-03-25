from rest_framework import serializers
from .models import Candidate, Resume


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
        read_only_fields = ["file_name", "uploaded_at"]

    def validate_ai_extracted_skills(self, value):
        if not value:
            raise serializers.ValidationError("AI extracted skills must not be empty.")
        return value

    def create(self, validated_data):
        uploaded_file = validated_data.get("file")
        if uploaded_file and "file_name" not in validated_data:
            validated_data["file_name"] = uploaded_file.name
        return super().create(validated_data)


class CandidateSerializer(serializers.ModelSerializer):
    resumes = ResumeSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "created_at",
            "resumes",
        ]
        read_only_fields = ["created_at"]