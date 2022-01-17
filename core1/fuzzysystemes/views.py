from django.shortcuts import render, HttpResponse
from . models import Celcius, Output
from rest_framework.views import APIView
from . serializers import CelcirusSerializer, OutputSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


class createOutput(APIView):
    def get(self, request):
        output = Output.objects.all().last()
        serializer = OutputSerializer(instance=output)
        if output:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No data", status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = OutputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


def data(request):
    return render(request, 'index.html')


@csrf_exempt
def createCelcius(request, humidity, roomtemperature, oventemperature):
    celcius = Celcius(humidity=humidity, temeperature=roomtemperature, oventemperature=oventemperature)
    celcius.save()
    serializer = CelcirusSerializer(celcius)
    if serializer:
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
    return HttpResponse(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class home(APIView):
    def get(self, request):
        celcius = Celcius.objects.all()
        serializer = CelcirusSerializer(celcius, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if request.data:
            serializer = CelcirusSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        return Response('No data in here')