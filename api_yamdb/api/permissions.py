from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.is_admin:
            return True


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.is_moderator:
            return True


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_admin:
            return True
