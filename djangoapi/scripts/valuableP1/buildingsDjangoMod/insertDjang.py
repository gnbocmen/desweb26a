
from django.contrib.gis.geos import GEOSGeometry 

from risk.models import Buildings
from scripts.valuableP1.myLib import p1Settings

def run():

    g=GEOSGeometry('POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))', srid=4326)
    #print the representation of the object
    if g.valid:
        print('geometria válida')
    print(g)
    #create a building object, from the model Buildings
    b=Buildings(description='Edificio 1', area=g.area, perimeter=g.length, year=2026, geom=g)

    #para guardar en base de datos es con save.
    b.save()
    #prints the asigned id of the object in the database
    print(b.id)
    #another way to create the object with a dictionary
    d_of_values= {'description':'Edificio 1', 
                'area':g.area,
                'perimeter':g.length,
                'year':2025,
                'geom':g}

    #b2=Buildings(d_of_values)
    #b2.save()
    #print(b2,id)
