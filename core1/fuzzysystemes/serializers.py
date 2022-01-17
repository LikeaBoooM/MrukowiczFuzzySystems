
from rest_framework import serializers
from .models import Celcius, Output


class CelcirusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celcius
        fields = '__all__'


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = '__all__'
