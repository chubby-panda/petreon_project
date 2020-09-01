from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/register/', views.CustomUserCreate.as_view()),
    path('users/account/<int:pk>/', views.CustomUserDetail.as_view()),
    path('users/profile/<int:pk>/', views.UserProfileDetail.as_view()),
    path('users/account/<int:pk>/change-password', views.ChangePasswordView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
