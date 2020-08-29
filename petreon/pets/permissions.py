from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.method)
        # Safe methods, e.g. GET
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsNotOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.pet.owner != request.user