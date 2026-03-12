from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Limit_politic
from scripts.valuabP1_djang.myLib import p1settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class limite_politic():
    def insert(self, d:dict):
        #we first get the snapped wkb format for the geometry:
        cur=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        cur.execute(query, [d['geom'],EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
        if g.valid:
            print("Geometría válida")
        else:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        #check if the geometry intersects any existing building
        query=""" 
            select id from risk_Limit_politic where ST_relate(
                geom,
                %s,
                'T********'
            ) and ID != 1
        """
        cur.execute(query, [snapped_wkb_geometry])
        r=cur.fetchall()

        if len(r)>0:
            return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        d['geom']=g
        d['area']=g.area
        d['perimeter']=g.length
        b=Limit_politic(**d)
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Building inserted', 'data': [d]}

    def update(self, d:dict):
        cur=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        cur.execute(query, [d['geom'],EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
        if g.valid:
            print("Geometría válida")
        else:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        #check if the geometry intersects any existing building
        query=""" 
            select id from buildings2_buildings where ST_relate(
                geom,
                %s,
                'T********'
            )
        """
        cur.execute(query, [snapped_wkb_geometry])
        r=cur.fetchall()

        if len(r)>0:
            pass
            #return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        #create the geometry with geos
        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)>0:
            b:Limit_politic=l[0]
        else:
            return {'ok':False, "Mesage": f"No buildings found with id {d['d'], 'data':None}"}

        b.geom=g
        b.description=d['description']
        b.height=d["height"]
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated buildings: {len(l)}",
                'data':[d]}


    def select(d:dict):
    #create the geometry with geos
        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        b:Limit_politic=l[0]
        d=model_to_dict(b)
        g=GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok':True, 'Message': f"Retriewed buildings: {len(l)}",
                'data':[d]}

    def delete(d:dict):

        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No buildings with the id {d['id']}", "data":None}
        b:Limit_politic=l[0]
        b.delete()
        return {'ok':True, 'Message': f"Buildings deleted: 1",
                'data':[{'id':d["id"]}]}



    def run():
        d_of_values= {
            'description':'Edificio 1', 
            'height':100, 
            'area':2000,
            'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
        }
        
        print(insert(d=d_of_values))
    
    
