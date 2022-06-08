from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на админа и суперюзера."""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_staff)
        )
