from django.db import models

# Create your models here.


class Celcius(models.Model):
    humidity = models.FloatField(max_length=100)
    temeperature = models.FloatField(max_length=100)
    oventemperature = models.IntegerField()

    def __str__(self):
        return str(self.temeperature)


class Output(models.Model):
    value = models.FloatField(max_length=100)

    def __str__(self):
        return str(self.value)