from django.http import Http404
from django.db.models import Prefetch
import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
import io

from .models import Pet, Pledge, Category, PetImage
from .serializers import PetSerializer, PledgeSerializer, PetDetailSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly, IsNotOwnerOrReadOnly, IsSupporterOrReadOnly, IsSuperUser, IsSuperUserOrReadOnly


class PetList(generics.ListAPIView):
    """
    View for pet list endpoint.
    """
    parser_classes = (MultiPartParser,)
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]
    filterset_fields = ['pet_category',]

    def get_queryset(self):
        queryset = Pet.objects.all().filter(active=True)
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
    """
    View for pet detail endpoint (view one pet).
    """
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pet_pk):
        try:
            pet = Pet.objects.get(pk=pet_pk)
            self.check_object_permissions(self.request, pet)
            return pet
        except Pet.DoesNotExist:
            raise Http404
    
    def get(self, request, pet_pk):
        pet = self.get_object(pet_pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pet_pk):
        pet = self.get_object(pet_pk)
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

    def delete(self, request, pet_pk):
        pet = self.get_object(pet_pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class PetPledgeList(APIView):
    """
    View for pledge list endpoint (of specific pet).
    """
    permission_classes = [IsNotOwnerOrReadOnly]

    def get_object(self, pet_pk):
        try:
            pet = Pet.objects.get(pk=pet_pk)
            self.check_object_permissions(self.request, pet)
            return pet
        except Pet.DoesNotExist:
            raise Http404

    def get(self, request, pet_pk):
        pledges = Pledge.objects.all().filter(pet=self.get_object(pet_pk))
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request, pet_pk):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user, pet=self.get_object(pet_pk))
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PledgeDetail(APIView):
    """
    View for pledge detail endpoint.
    """

    permission_classes = [IsSupporterOrReadOnly,]

    def get_object(self, pledge_pk):
        try:
            pledge = Pledge.objects.get(pk=pledge_pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pet_pk, pledge_pk):
        pledge = self.get_object(pledge_pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pet_pk, pledge_pk):
        pledge = self.get_object(pledge_pk)
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

    def delete(self, request, pet_pk, pledge_pk):
        pledge = self.get_object(pledge_pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class CategoryList(APIView):
    """
    View for category list endpoint (all categories).
    """

    permission_classes = [IsSuperUserOrReadOnly]
    
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
    """
    View for category detail endpoint
    """

    permission_classes = [IsSuperUser]

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request, category)
            return category
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
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
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

