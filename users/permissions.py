from rest_framework import permissions

class IsModer(permissions.BasePermission):
    message = "Проверка на модератора"

    def has_permission(self, request, view):
         return request.user.groups.filter(name="moders").exists