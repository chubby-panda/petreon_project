from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    For use with pet model change views.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsNotOwnerOrReadOnly(permissions.BasePermission):
    """
    For use with pledge model create views.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print("This is working...")
            return True
        return obj.owner != request.user

class IsSupporterOrReadOnly(permissions.BasePermission):
    """
    For use with pledge model update views.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.supporter == request.user


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