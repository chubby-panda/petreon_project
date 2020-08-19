from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Pet, Pledge
from .serializers import PetSerializer, PledgeSerializer, PetDetailSerializer


class PetList(APIView):

    # This is the GET method, this passes the pets objects to the serializer and returns them as a response. Now to urls...
    def get(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PetSerializer(data=request.data)
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


class PetDetail(APIView):

    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetDetailSerializer(pet)
        return Response(serializer.data)


class PledgeList(APIView):

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