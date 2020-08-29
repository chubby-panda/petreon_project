from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Safe methods, e.g. GET
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.username == request.user

class IsNotLoggedIn(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            pass