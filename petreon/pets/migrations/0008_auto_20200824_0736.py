# Generated by Django 3.0.8 on 2020-08-24 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0007_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='pets.Category'),
        ),
    ]
