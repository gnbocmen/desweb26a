from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Limit_politic
from scripts.valuabP1_djang.myLib import p1settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class limite_politic_class():
    def insert(self, d:dict):
        #we first get the snapped wkb format for the geometry:
        cur=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, 4326),%s)"
        cur.execute(query, [d['geom'], ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        #print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=4326)
        
        if not g.valid:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        #check if the geometry intersects any existing building
        
        #verificamos que la geometría excepto la geometría de la región
        if d.get('id', -1) != 1:

            #verificamos que este dentro de la región:
            query_within = "SELECT ST_Within(%s::geometry, (SELECT geom FROM risk_limit_politic WHERE id = 1))"
            cur.execute(query_within, [snapped_wkb_geometry])
            r=cur.fetchall()
            if r and r[0][0] is False:
                return {'ok': False, 'message':'The geometry is not inside the region Huánuco (id=1)', 'data': None}

            #verificamos que no se intersecte
            query=""" 
                select id from risk_limit_politic where ST_relate(
                    geom,
                    %s,
                    'T********'
                ) and id != 1
            """
            cur.execute(query, [snapped_wkb_geometry])
            r=cur.fetchall()

            if len(r)>0:
                return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        #para el calculo del area y perimetro se transforma utm
        g_utm = g.transform(EPSG_FOR_GEOMETRIES, clone=True)
        d['geom']=g
        d['area']=g_utm.area
        d['perimeter']=g_utm.length
        b=Limit_politic(**d)
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Polígono inserted', 'data': [d]}

    def update(self, d:dict):
        cur=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, 4326),%s)"
        cur.execute(query, [d['geom'], ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=4326)
        if not g.valid:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        if d.get('id', -1) != 1:

            #verificamos que este dentro de la región:
            query_within = "SELECT ST_Within(%s::geometry, (SELECT geom FROM risk_limit_politic WHERE id = 1))"
            cur.execute(query_within, [snapped_wkb_geometry])
            r=cur.fetchall()
            if r and r[0][0] is False:
                return {'ok': False, 'message':'The geometry is not inside the region Huánuco (id=1)', 'data': None}

            #check if the geometry intersects any existing geometry
            query=""" 
                select id from risk_limit_politic where ST_relate(
                    geom,
                    %s,
                    'T********'
                ) AND id!=%s AND id != 1
            """
            cur.execute(query, [snapped_wkb_geometry, d['id']])
            r=cur.fetchall()

            if len(r)>0:
                return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        #create the geometry with geos
        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)>0:
            b:Limit_politic=l[0]
        else:
            return {'ok':False, "message": f"No Poligon found with id {d['id']}", 'data':None}

        #transformamos a utm para calcular area y perimetro
        g_utm = g.transform(EPSG_FOR_GEOMETRIES, clone=True)
        d['geom']=g
        d['area']=g_utm.area
        d['perimeter']=g_utm.length

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated Poligon: {len(l)}",
                'data':[d]}


    def selectAsDict(self, d:dict):
    #create the geometry with geos
        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        d=model_to_dict(b)
        d['geom']=writer.write(b.geom)
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok':True, 'Message': f"Retriewed Poligon: {len(l)}",
                'data':[d]}
        

    def selectAsTuples(self, d:dict):
    #create the geometry with geos
        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        geom_wkt=writer.write(b.geom)
        data_creation_str = b.data_creation.strftime("%Y-%m-%d %H:%M:%S")

        tup= (b.id, b.nombre, b.provincia, b.poblacion, b.area, b.perimeter, geom_wkt, data_creation_str)
        return {'ok':True, 'Message': f"Retrieved River as Tuple: {len(l)}", 
                'data':[tup]}

    def delete(self, d:dict):

        f=Limit_politic.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No Poligon with the id {d['id']}", "data":None}
        b:Limit_politic=l[0]
        b.delete()
        return {'ok':True, 'Message': f"Poligon deleted: 1",
                'data':[{'id':d["id"]}]}



    

