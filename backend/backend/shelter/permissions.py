from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.lower() == 'admin'


class IsUser(permissions.BasePermission):
    """
    Allows access only to users with the 'user' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.lower() == 'user'


class IsSpecificRole(permissions.BasePermission):
    """
    Allows access only to users with specific roles.
    Specify allowed roles in `view.allowed_roles`.
    """
    def has_permission(self, request, view):
        allowed_roles = getattr(view, 'allowed_roles', [])
        return request.user and request.user.is_authenticated and request.user.role.lower() in map(str.lower, allowed_roles)
