from rest_framework.permissions import BasePermission

from core.users.models import User


class IsAdmin(BasePermission):
    """Permission Class for Admin users"""

    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN.value
