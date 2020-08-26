from rest_framework import serializers
from .models import CustomUser
from pets.models import Category


# This is the CustomUser serializer that will handle the inputted data and pass it to the database, and then return the data as an object
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user