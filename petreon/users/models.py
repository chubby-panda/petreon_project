import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    """
    Model for user authentication/account.
    """
    pass

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    Model for user profile.
    """
    def upload_image_to(instance, filename):
        print(filename)
        filename_base, filename_ext = os.path.splitext(filename)
        print(os.path.splitext(filename))
        u = uuid.uuid4()
        return 'posts/profiles/%s' % (
            u.hex
        )

    profile_img = models.ImageField(
        upload_to=upload_image_to, editable=True, null=True, blank=True, default='default.jpg')
    fun_fact = models.CharField(max_length=200)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
    )

    class Meta:
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, **kwargs):
    """
    Signal to create profile object when user object is created
    """
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=CustomUser)
