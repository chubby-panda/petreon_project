from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.method)
        # Safe methods, e.g. GET
        if request.method in permissions.SAFE_METHODS:
            return True
        print('object', obj)
        print('user', request.user)
        return obj == request.user


class IsSuperUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)


class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


