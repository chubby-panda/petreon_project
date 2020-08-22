from django.db import models


"""This is the Pet model (project for each pet surgery). After defining it here, we make migrations, migrate and then create a serializer to handle it."""
class Pet(models.Model):
    title = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    description = models.TextField()
    med_treatment = models.CharField(max_length=100, verbose_name="medical treatment")
    date_created = models.DateTimeField(auto_now_add=True)
    goal = models.IntegerField()
    active = models.BooleanField(default=True)
    owner = models.CharField(max_length=100)
    category = models.CharField(max_length=100)


"""This is the Pledge model. Note: we don't want the pet owner to be able to update pledges to their pet."""
class Pledge(models.Model):
    pet = models.ForeignKey(
        'Pet',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    amount = models.IntegerField()
    anonymous = models.BooleanField(default=False)
    supporter = models.CharField(max_length=100)