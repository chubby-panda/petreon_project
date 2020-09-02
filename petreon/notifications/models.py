from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    """
    Model for notifications.
    """
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=500)
    date_sent = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    class Meta:
        ordering = ['-date_sent',]