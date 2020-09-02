from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationList(APIView):
    """
    View for notifications list endpoint.
    """
    serializer = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.all().filter(recipient=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)