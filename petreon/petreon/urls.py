from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', include('pets.urls')),
    path('', include('users.urls')),
    # This puts the login button on the page
    path('api-auth/', include('rest_framework.urls')),
    # This is to generate a token for authentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
