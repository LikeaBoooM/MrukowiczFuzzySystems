from rest_framework import serializers
from .models import Celcius


class CelcirusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celcius
        fields = '__all__'
