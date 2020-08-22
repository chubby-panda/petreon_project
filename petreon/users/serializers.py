from rest_framework import serializers
from .models import CustomUser


# This is the CustomUser serializer that will handle the inputted data and pass it to the database, and then return the data as an object
class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)
