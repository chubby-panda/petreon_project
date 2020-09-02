from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification model.
    """
    date_sent = serializers.DateTimeField(read_only=True)
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Notification
        fields = ('id', 'title', 'body', 'date_sent', 'recipient')

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)