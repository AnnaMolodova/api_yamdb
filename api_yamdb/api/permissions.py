from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CommentReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin
                    or request.user == obj.author
                    or request.user.is_moderator))


class AdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS)


class Admin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


class AuthorAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'DELETE'
                and request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.user.is_authenticated
                and request.user.is_superuser)
