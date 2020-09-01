from django.contrib import admin
from .models import Pet, Pledge, Category

# Register your models here.
admin.site.register(Pet)
admin.site.register(Pledge)
admin.site.register(Category)