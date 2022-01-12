from django.shortcuts import render
from . models import Celcius
from rest_framework.views import APIView
from . serializers import CelcirusSerializer
from rest_framework.response import Response
from rest_framework import status


def data(request):
    return render(request, 'index.html')

class home(APIView):
    def get(self, request):
        celcius = Celcius.objects.all()
        serializer = CelcirusSerializer(celcius, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if request.data:
            serializer = CelcirusSerializer(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        return Response('No data in here')