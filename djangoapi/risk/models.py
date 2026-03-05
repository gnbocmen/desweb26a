from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class Buildings(models.Model):

    description = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter =models.FloatField(blank=True, null=True)
    year =models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)


#añadiendo esto solo conectaría a la tabla y no haría ningún cambio a los campos.
    # class meta:
    #     manage = False
