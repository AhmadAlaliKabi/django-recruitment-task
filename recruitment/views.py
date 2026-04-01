#views.py
"""
Purpose:
    API/view layer for public jobs, internal jobs, candidate CRUD, resume CRUD, and cache test.

Connects with:
    - models.py for all data access
    - serializers.py for DRF model viewsets
    - urls_public.py / urls_internal.py / drf_urls.py / project urls.py for routing
"""

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError

from .models import JobPosting, Candidate
from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.permissions import IsAuthenticated

# recruitment/views.py

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    # DRF endpoint for uploading/listing/updating resumes (supports multipart file upload).
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]
class CandidateViewSet(viewsets.ModelViewSet):
    # Auth-protected candidate CRUD for internal API users.
    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

class PublicJobListView(View):
    # Public endpoint: only active jobs.
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
    # Public endpoint: accepts simple JSON application and creates Candidate record.
    def post(self, request):
        try:
            data = json.loads(request.body)

            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            phone = data.get("phone", "")

            if not first_name or not last_name or not email:
                return JsonResponse(
                    {"error": "first_name, last_name, and email are required."},
                    status=400
                )

            candidate = Candidate.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )

            return JsonResponse(
                {
                    "message": "Application submitted successfully.",
                    "candidate_id": candidate.id,
                },
                status=201
            )
        except IntegrityError:
            return JsonResponse(
                {"error": "A candidate with this email already exists."},
                status=409
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)


class InternalJobListView(View):
    # Internal endpoint: includes is_active state for all jobs.
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
from django.http import JsonResponse
from django.core.cache import cache


def test_redis_cache(request):
    # Quick health-check for Redis cache wiring.
    cache.set("test_key", "Redis is working", timeout=60)
    value = cache.get("test_key")

    return JsonResponse({
        "cached_value": value
    })
