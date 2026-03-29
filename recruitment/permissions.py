from rest_framework.permissions import BasePermission


class IsDepartmentHead(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff