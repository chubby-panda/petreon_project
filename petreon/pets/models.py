from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "categories"


def get_generic_category():
    return Category.objects.get_or_create(category='pet')[0]


class Pet(models.Model):
    title = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    description = models.TextField()
    med_treatment = models.CharField(max_length=100, verbose_name="medical treatment")
    date_created = models.DateTimeField(auto_now_add=True)
    goal = models.IntegerField()
    pledged_amount = models.IntegerField(default=0)
    goal_reached = models.BooleanField(default=False)
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

    class Meta:
        ordering = ['-date_created',]

    def __str__(self):
        return self.title


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

    def __str__(self):
        return str(self.supporter)

def get_total_pledge(sender, instance, **kwargs):
    if kwargs:
        p = instance.pet
        p.pledged_amount += instance.amount
        if p.pledged_amount >= p.goal:
            p.goal_reached = True
        p.save()

post_save.connect(get_total_pledge, sender=Pledge)