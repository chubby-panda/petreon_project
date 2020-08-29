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