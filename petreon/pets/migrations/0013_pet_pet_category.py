# Generated by Django 3.0.8 on 2020-08-26 10:23

from django.db import migrations, models
import pets.models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0012_remove_pet_pet_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='pet_category',
            field=models.ForeignKey(default=0, on_delete=models.SET(pets.models.get_generic_category), related_name='pets', to='pets.Category'),
            preserve_default=False,
        ),
    ]
