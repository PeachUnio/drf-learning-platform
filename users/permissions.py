from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = "Проверка на модератора"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsAuth(permissions.BasePermission):
    """Проверяет, является ли пользователь автором."""

    def has_object_permission(self, request, view, obj):
        if obj.auth == request.user:
            return True
        return False
