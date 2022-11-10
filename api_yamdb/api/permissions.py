from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from reviews.models import Role


class CommentReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == Role.ADMIN
            or request.user.role == Role.MODERATOR
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif (request.user.is_anonymous and request.method != ['POST',
              'PATCH', 'DELETE']):
            return True
        elif request.user.role == Role.ADMIN:
            return True
        else:
            return False


class Admin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


class AuthorAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == Role.ADMIN
        )
