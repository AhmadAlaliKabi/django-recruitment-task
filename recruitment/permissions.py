"""
Purpose:
    Custom DRF permissions for role-based checks.

Connects with:
    - DRF views/viewsets when this permission is attached
"""

from rest_framework.permissions import BasePermission


class IsDepartmentHead(BasePermission):
    # Current rule: any staff user passes.
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
