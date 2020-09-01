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
    profile_img = models.ImageField(upload_to='images/', default='default.jpg')
    fun_fact = models.CharField(max_length=200)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name = 'profile',
    )

    class Meta:
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=CustomUser)