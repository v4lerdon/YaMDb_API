from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на админа и суперюзера."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Проверка на автора, админа или модератора."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_authenticated and request.user.is_moderator
            or request.user.is_authenticated and obj.author == request.user
            or request.user.is_authenticated and request.method == 'POST'
        )
