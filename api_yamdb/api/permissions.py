from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Пермишн только для админа."""

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.is_admin
                )


class AdminPermissionOrReadOnly(BasePermission):
    """Пермишн для админа, суперадмина,
     и для авторизованного пользователя для метода гет."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or request.user.is_authenticated
                and request.user.is_admin
                )


class ReviewPermission(BasePermission):
    """Пермишн для Ревью и Комментариев."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin or request.user.is_moderator
                )
