from django.contrib import admin
from .models import Pet, Pledge, Category


admin.site.register(Pet)
admin.site.register(Pledge)
admin.site.register(Category)