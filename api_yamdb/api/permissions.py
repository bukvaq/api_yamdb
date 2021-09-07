from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserRoles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.role == UserRoles.ADMIN)


class AdminPermissionOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_authenticated and
                (request.user.role == UserRoles.ADMIN
                 or request.user.is_superuser)
                )
