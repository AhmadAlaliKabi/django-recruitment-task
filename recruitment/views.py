"""
Views for public APIs, internal APIs, and DRF viewsets.
"""

import json

from django.core.cache import cache
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Candidate, JobPosting, Resume
from .salary_predictor import predict_salary
from .serializers import CandidateSerializer, ResumeSerializer, SalaryPredictionInputSerializer


class PublicJobListView(View):
    """Public endpoint: list active jobs only."""

    def get(self, request):
        jobs = JobPosting.objects.filter(is_active=True).values(
            "id",
            "title",
            "description",
            "location",
            "posted_at",
        )
        return JsonResponse({"jobs": list(jobs)}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class JobApplicationView(View):
    """Public endpoint: accept JSON application and create a candidate."""

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        phone = data.get("phone", "")

        if not first_name or not last_name or not email:
            return JsonResponse(
                {"error": "first_name, last_name, and email are required."},
                status=400,
            )

        try:
            candidate = Candidate.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
        except IntegrityError:
            return JsonResponse(
                {"error": "A candidate with this email already exists."},
                status=409,
            )

        return JsonResponse(
            {
                "message": "Application submitted successfully.",
                "candidate_id": candidate.id,
            },
            status=201,
        )


class InternalJobListView(View):
    """Internal endpoint: list all jobs including active/inactive status."""

    def get(self, request):
        jobs = JobPosting.objects.all().values(
            "id",
            "title",
            "description",
            "location",
            "is_active",
            "posted_at",
        )
        return JsonResponse({"internal_jobs": list(jobs)}, status=200)


class CandidateViewSet(viewsets.ModelViewSet):
    """Protected candidate CRUD API (JWT required)."""

    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["view"] = self
        return context


class ResumeViewSet(viewsets.ModelViewSet):
    """Protected resume CRUD API with multipart file upload support."""

    queryset = Resume.objects.all().order_by("-uploaded_at")
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]


def test_redis_cache(request):
    """Simple Redis cache health-check endpoint."""

    cache.set("test_key", "Redis is working", timeout=60)
    return JsonResponse({"cached_value": cache.get("test_key")})


class SalaryPredictionView(APIView):
    """
    Internal POST API that predicts salary from model features.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SalaryPredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            predicted_salary = predict_salary(serializer.validated_data)
        except FileNotFoundError as exc:
            return Response(
                {"success": False, "error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            return Response(
                {"success": False, "error": f"Prediction failed: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "predicted_monthly_salary": predicted_salary,
                "input": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )
