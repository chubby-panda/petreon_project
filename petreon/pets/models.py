from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    category = models.CharField(max_length=100)


def get_generic_category():
    return Category.objects.get_or_create(category='pet')[0]


class Pet(models.Model):
    title = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    description = models.TextField()
    med_treatment = models.CharField(max_length=100, verbose_name="medical treatment")
    date_created = models.DateTimeField(auto_now_add=True)
    goal = models.IntegerField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_pets'
    )
    pet_category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_generic_category), 
        related_name='pets'
    )


class Pledge(models.Model):
    pet = models.ForeignKey(
        'Pet',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    amount = models.IntegerField()
    anonymous = models.BooleanField(default=False)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )
