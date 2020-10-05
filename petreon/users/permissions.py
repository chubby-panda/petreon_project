from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    For use with profile/user/password change views.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsProfileUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsSuperUserOrReadOnly(permissions.IsAdminUser):
    """
    For use with admin-level change views.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)


class IsSuperUser(permissions.IsAdminUser):
    """
    For use with admin-level access views.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
