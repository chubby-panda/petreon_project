from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.create(user=instance)