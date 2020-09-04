from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser

from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, ChangePasswordSerializer, UserProfileSerializer
from .permissions import IsUserOrReadOnly, IsSuperUser


class CustomUserCreate(generics.CreateAPIView):
    """
    View for registering new account.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def check_permissions(self, request):
        if request.user.is_authenticated:
            self.permission_denied(request)


class ChangePasswordView(generics.UpdateAPIView):
    """
    A view for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsUserOrReadOnly,)

    def get_object(self, queryset=None):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserList(APIView):
    """
    View for user list endpoint (admin use only).
    """

    permission_classes = [IsSuperUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CustomUserDetail(APIView):
    """
    View for user account detail endpoint.
    """

    permission_classes = [IsUserOrReadOnly]

    def get_object(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(username=self.get_object(pk))
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class UserProfileDetail(APIView):
    """
    View for profile detail endpoint.
    """
    permission_classes = [IsUserOrReadOnly,]
    parser_classes = (MultiPartParser,)
    serializer_class = UserProfileSerializer

    def get_object(self, pk):
        try:
            profile = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist():
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 