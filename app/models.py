from django.db import models

# Create your models here.
class ModelInput(models.Model):
    horizontalSpatialCoordinate = models.IntegerField()
    verticalSpatialCoordinate = models.IntegerField()
    ffmcIndex = models.FloatField()
    dmcIndex = models.FloatField()
    dcIndex = models.FloatField()
    isi = models.FloatField()
    temperature = models.FloatField()
    relativeHumidity = models.FloatField()
    wind = models.FloatField()
    rain = models.FloatField() 

class ModelOutput(models.Model):
    modelInput = models.ForeignKey(ModelInput, on_delete=models.CASCADE)
    area = models.FloatField()