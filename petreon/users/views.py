from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, ChangePasswordSerializer, UserProfileSerializer, UserPetSerializer, ProfileImageSerializer
from .permissions import IsUserOrReadOnly, IsSuperUser, IsProfileUserOrReadOnly
from pets.models import Pet
from pets.serializers import PetSerializer


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

    def get_object(self, username):
        user = CustomUser.objects.get(username=username)
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

    def get_object(self, username):
        try:
            user = CustomUser.objects.get(username=username)
            self.check_object_permissions(self.request, user)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_object(username)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(username=self.get_object(username))
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetail(APIView):
    """
    View for profile detail endpoint.
    """
    permission_classes = [IsProfileUserOrReadOnly, ]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserProfileSerializer

    def get_object(self, username):
        try:
            profile = UserProfile.objects.select_related(
                'user').get(user__username=username)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist():
            raise Http404

    def get(self, request, username):
        profile = self.get_object(username=username)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, username):
        profile = self.get_object(username)
        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True)
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

    def delete(self, request, username):
        profile = self.get_object(username)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditProfileImageView(APIView):
    """
    View to update profile image
    """
    # permission_classes = [IsProfileUserOrReadOnly, ]
    parser_classes = [FileUploadParser, ]
    serializer_class = ProfileImageSerializer

    def get_object(self, username):
        try:
            profile = UserProfile.objects.select_related(
                'user').get(user__username=username)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist():
            raise Http404

    def get(self, request, username):
        profile = self.get_object(username=username)
        serializer = ProfileImageSerializer(profile)
        return Response(serializer.data)

    def put(self, request, username):
        print("REQUEST:", request.data['file'])
        profile = self.get_object(username)
        serializer = ProfileImageSerializer(
            profile, data={'image': request.data['file']})
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


class UserPetList(APIView):
    """
    View for pet list endpoint (of specific user).
    """

    def get_object(self, username):
        try:
            user = CustomUser.objects.get(username=username)
            self.check_object_permissions(self.request, user)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username):
        pets = Pet.objects.all().filter(owner=self.get_object(username))
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
