from rest_framework import permissions


class IsAuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
            or request.user.is_admin 
            or reques.user.role == 'moderator'):
                return True
        return obj.author == request.user
