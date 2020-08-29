from django.http import Http404
from django.db.models import Prefetch
import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from .models import Pet, Pledge, Category
from .serializers import PetSerializer, PledgeSerializer, PetDetailSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly, IsNotOwnerOrReadOnly

# def get_choice_set(model):
#     pet_tuple = []
#     for o in model.objects.all():
#         p = o.pet_category
#         pt = (p, p)
#         pet_tuple.append(pt)
#     pet_tuple = tuple(pet_tuple)
#     print(pet_tuple)
#     return pet_tuple

# class PetFilter(filters.FilterSet):
#     pet_category = filters.ChoiceFilter(choices=get_choice_set(Pet))

#     class Meta:
#         model = Pet
#         fields = ('pet_category', 'owner',)


# Changed APIView to GenericAPIView (10:15)
class PetList(generics.ListAPIView):
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]
    # filter_backends = [filters.DjangoFilterBackend]
    # filter_class = PetFilter
    filterset_fields = ['pet_category',]

    def get_queryset(self):
        queryset = Pet.objects.all()
        category = self.request.query_params.get('pet_category', None)
        if category is not None:
            queryset = queryset.filter(pet_category__category=category)
        return queryset

    def get(self, request):
        pets = self.get_queryset()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PetDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            pet = Pet.objects.get(pk=pk)
            self.check_object_permissions(self.request, pet)
            return pet
        except Pet.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetDetailSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class PledgeList(APIView):

    permission_classes = [IsNotOwnerOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PledgeDetail(APIView):


    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )    
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryDetail(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)