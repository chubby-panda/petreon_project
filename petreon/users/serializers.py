from rest_framework import serializers

from .models import CustomUser, UserProfile
from pets.models import Pet


class UserPetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Pet
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile endpoint.
    """
    id = serializers.ReadOnlyField()
    profile_img = serializers.ImageField()
    fun_fact = serializers.CharField(max_length=200)
    user = serializers.ReadOnlyField(source='user.username')
    username = serializers.ReadOnlyField(source='user.username')
    pets = UserPetSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'profile_img', 'fun_fact', 'user', 'username', 'pets')

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.fun_fact = validated_data.get('fun_fact', instance.fun_fact)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user endpoint.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

