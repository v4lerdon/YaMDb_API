from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на админа и суперюзера."""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_staff)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Проверка на автора, админа или модератора."""
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (
                request.user.is_staff or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user
                or request.method == 'POST' and request.user.is_authenticated
            ):
                return True
