from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import JobPosting, Candidate
from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.permissions import IsAuthenticated


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

class PublicJobListView(View):
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

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)


class InternalJobListView(View):
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