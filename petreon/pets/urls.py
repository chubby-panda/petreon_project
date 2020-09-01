from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('pets/', views.PetList.as_view()),
    path('pets/<int:pet_pk>/', views.PetDetail.as_view()),
    path('pets/category/', views.CategoryList.as_view()),
    path('pets/category/<int:pk>/', views.CategoryDetail.as_view()),
    path('pets/<int:pet_pk>/pledges/', views.PetPledgeList.as_view()),
    path('pets/<int:pet_pk>/pledges/<int:pledge_pk>/', views.PledgeDetail.as_view()),
]

# This is like the include function
urlpatterns = format_suffix_patterns(urlpatterns)

