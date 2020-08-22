from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('pets.urls')),
    path('', include('users.urls')),
    # This puts the login button on the page
    path('api-auth/', include('rest_framework.urls')),
]
