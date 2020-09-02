from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('pets/', views.PetList.as_view()), # View all pets, category filter
    path('pets/<int:pet_pk>/', views.PetDetail.as_view()), # View one pet
    path('pets/category/', views.CategoryList.as_view()), # View all categories
    path('pets/category/<int:pk>/', views.CategoryDetail.as_view()), # View a category
    path('pets/<int:pet_pk>/pledges/', views.PetPledgeList.as_view()), # View all pledges for one pet
    path('pets/<int:pet_pk>/pledges/<int:pledge_pk>/', views.PledgeDetail.as_view()), # View one pledge for one pet
]

urlpatterns = format_suffix_patterns(urlpatterns)

