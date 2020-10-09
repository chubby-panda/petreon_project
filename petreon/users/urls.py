from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/', views.CustomUserList.as_view()),  # View all users
    path('users/register/', views.CustomUserCreate.as_view()),  # Register
    path('users/account/<str:username>/',
         views.CustomUserDetail.as_view()),  # View account
    path('users/profile/<str:username>/',
         views.UserProfileDetail.as_view()),  # View profile
    path('users/<str:username>/pets/', views.UserPetList.as_view()),
    path('users/account/<int:pk>/change-password/',
         views.ChangePasswordView.as_view()),  # Change password
]

urlpatterns = format_suffix_patterns(urlpatterns)
