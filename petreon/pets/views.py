from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Pet, Pledge, Category
from .serializers import PetSerializer, PledgeSerializer, PetDetailSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


class PetList(APIView):
    # This means if I'm logged in, I have permissions. If I'm not, then it will be read-only.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]

    # This is the GET method, this passes the pets objects to the serializer and returns them as a response. 
    def get(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    # This is the POST method; this passes a pet object to the serializer, which saves it in the database as a new object.
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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]

    # This is our GET_OBJECT method we created - it returns an object by pk
    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404
    
    # GET
    def get(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetDetailSerializer(pet)
        return Response(serializer.data)

    # This is the PUT method, this retrieves the pet object using .get_object, then passes the updated pet object to the serializer and returns it as a response.
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

    # This is the DELETE method, this passes a pk as a request and deletes it. No serializer is required, because there is no json data in the request.
    def delete(self, request, pk):
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class PledgeList(APIView):


    # GET
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    # POST (create)
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
            return Pledge.objects.get(pk=pk)
        except Pledge.DoesNotExist:
            raise Http404

    # GET
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    # PUT (update)
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

    # DELETE
    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# This is the CategoryList view that will show a list of all the categories available (those with admin privileges will be able to create/update/delete categories)
class CategoryList(APIView):
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)