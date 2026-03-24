from django.db import models
from django.contrib.gis.db import models as gis_models
import django.utils.timezone as djangoTimezone

##crear app
#python manage.py startapp risk

##migracion
##python manage.py makemigrations
##python manage.py migrate 

# Create your models here.
class Points_crit(models.Model):

    nombre = models.CharField(max_length=100, blank=True, null=True)
    fuente = models.CharField(max_length=100, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    year =models.FloatField(blank=True, null=True)
    geom = gis_models.PointField(srid=4326, blank=True, null=True)
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

    def save(self, *args, **kwargs):
            # Calculate values from the geometry before saving
            # if self.geom:
            #     # Transformamos temporalmente a UTM (32718) para medir en metros
            #     geom_utm = self.geom.transform(32718, clone=True)
            #     self.area = geom_utm.area
            #     self.perimeter = geom_utm.length
            
            super().save(*args, **kwargs)

class Rivers(models.Model):

    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    vertiente = models.CharField(max_length=100, blank=True, null=True)
    longitud =models.FloatField(blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    geom = gis_models.LineStringField(srid=4326, blank=True, null=True)
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

    def save(self, *args, **kwargs):
            # Calculate values from the geometry before saving
            if self.geom:
                # Transformamos temporalmente a UTM (32718) para medir en metros
                geom_utm = self.geom.transform(32718, clone=True)
                #self.area = geom_utm.area
                self.perimeter = geom_utm.length
            
            super().save(*args, **kwargs)

class Limit_politic(models.Model):

    nombre = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter =models.FloatField(blank=True, null=True)
    poblacion =models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=4326, blank=True, null=True)
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

    def save(self, *args, **kwargs):
            # Calculate values from the geometry before saving
            if self.geom:
                # Transformamos temporalmente a UTM (32718) para medir en metros
                geom_utm = self.geom.transform(32718, clone=True)
                self.area = geom_utm.area
                self.perimeter = geom_utm.length
            
            super().save(*args, **kwargs)

#añadiendo esto solo conectaría a la tabla y no haría ningún cambio a los campos.
    # class meta:
    #     manage = False
