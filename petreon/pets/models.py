from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from notifications.models import Notification


class Category(models.Model):
    """
    Model for category.
    """
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "categories"


def get_generic_category():
    """
    Set a generic category if a category object is deleted.
    """
    return Category.objects.get_or_create(category='pet')[0]


class Pet(models.Model):
    """
    Model for pets/projects.
    """
    title = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', default='media/default.jpg')
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


class PetImage(models.Model):
    """
    Model for pet images. Separate model created so that multiple images can be uploaded for each pet instance. 
    """
    image = models.ImageField(upload_to='images/', max_length=254)
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return self.image.name


class Pledge(models.Model):
    """
    Model for pledges.
    """
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


def get_pledge_update(sender, instance, **kwargs):
    """
    Signal to send notification when pledge object is created/updated.
    """
    s = instance.supporter
    if instance.anonymous:
        s = "An anonymous supporter"
    if kwargs['created']:
        Notification.objects.create(
            title=f"Your pet {instance.pet.pet_name} has received a pledge.",
            body=f"{s} has pledged ${instance.amount} to your pet, {instance.pet.pet_name}.",
            recipient=instance.pet.owner
            )
    elif kwargs['created'] is False:
        Notification.objects.create(
            title=f"{s} updated their pledge for {instance.pet.pet_name}.",
            body=f"{s} has changed their original pledge for {instance.pet.pet_name}'s treatment to ${instance.amount}.",
            recipient=instance.pet.owner
        )

post_save.connect(get_pledge_update, sender=Pledge)


def get_total_pledge(sender, instance, **kwargs):
    """
    Signal to change pet values when pledge object is created/put/deleted
    """
    if kwargs:
        instance.pet.pledged_amount += instance.amount
        if instance.pet.pledged_amount >= instance.pet.goal:
            instance.pet.goal_reached = True
            Notification.objects.create(
                title=f"Goal reached!",
                body=f"Congratulations! {instance.pet.pet_name}'s treatment has been fully funded.",
                recipient=instance.pet.owner
            )
            instance.pet.active = False
        instance.pet.save()

post_save.connect(get_total_pledge, sender=Pledge)