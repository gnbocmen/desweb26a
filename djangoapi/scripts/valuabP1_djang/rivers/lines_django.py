from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Rivers
from scripts.valuabP1_djang.myLib import p1settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Rivers_class():
    def insert(self, d:dict):
        #we first get the snapped wkb format for the geometry:
        cur=connection.cursor()
        query="select st_snaptogrid(st_transform(st_geomfromtext(%s, 32718), 4326), %s)"
        cur.execute(query, [d['geom'], ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        #print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=4326)
        
        if not g.valid:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        #check if the geometry intersects any existing building     

        #verificamos que este dentro de la región:
        query_within = "SELECT ST_Within(%s::geometry, (SELECT geom FROM risk_limit_politic WHERE id = 1))"
        cur.execute(query_within, [snapped_wkb_geometry])
        r=cur.fetchall()
        if r and r[0][0] is False:
            return {'ok': False, 'message':'The river is not inside the region Huánuco (id=1)', 'data': None}

        #verificamos que no se intersecte
        query=""" 
            select id from risk_rivers where ST_relate(
                geom,
                %s,
                'T********'
            ) 
        """
        cur.execute(query, [snapped_wkb_geometry])
        r=cur.fetchall()

        if len(r)>0:
            return {'ok': False, 'message':'The river intersects with others rivers id', 'data': r}

        #para el calculo del area y perimetro se transforma utm
        g_utm = g.transform(EPSG_FOR_GEOMETRIES, clone=True)
        d['geom']=g
        d['longitud']=g_utm.length
        b=Rivers(**d)
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Polígono inserted', 'data': [d]}

    def update(self, d:dict):
        cur=connection.cursor()
        query="select st_snaptogrid(st_transform(st_geomfromtext(%s, 32718), 4326), %s)"
        cur.execute(query, [d['geom'], ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        #now we can check if it is valid as before:
        g=GEOSGeometry(snapped_wkb_geometry, srid=4326)
        if not g.valid:
            return {'ok': False, 'message':'Invalid geometry', 'data': None}
        
        #Now we can check if it intersects with another geomtry in the same layer
        
        #verificamos que este dentro de la región:
        query_within = "SELECT ST_Within(%s::geometry, (SELECT geom FROM risk_limit_politic WHERE id = 1))"
        cur.execute(query_within, [snapped_wkb_geometry])
        r=cur.fetchall()
        if r and r[0][0] is False:
            return {'ok': False, 'message':'The river is not inside the region Huánuco (id=1)', 'data': None}

        #check if the geometry intersects any existing geometry
        query=""" 
            select id from risk_rivers where ST_relate(
                geom,
                %s,
                'T********'
            ) AND id!=%s 
        """
        cur.execute(query, [snapped_wkb_geometry, d['id']])
        r=cur.fetchall()

        if len(r)>0:
            return {'ok': False, 'message':'The river intersects with others rivers id', 'data': r}

        #create the geometry with geos
        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)>0:
            b:Rivers=l[0]
        else:
            return {'ok':False, "message": f"No River was found with id {d['id']}", 'data':None}

        #transformamos a utm para calcular area y perimetro
        g_utm = g.transform(EPSG_FOR_GEOMETRIES, clone=True)
        d['geom']=g
        d['longitud']=g_utm.length

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated Poligon: {len(l)}",
                'data':[d]}


    def select(self, d:dict, asDict=False):
    #create the geometry with geos
        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        
        writer = WKTWriter(precision=4)
        if asDict:
            dc = list(f.values( ))

            for i in dc:
                if i.get('geom'):
                    i['geom'] = writer.write(i['geom'])
                if i.get('data_creation'):
                    i['data_creation'] = i['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
            return {'ok':True, 'Message': f"Retriewed Poligon: {len(l)}",
                'data':dc}

        else:

            b=f.first()
            b:Rivers=l[0]
            d=model_to_dict(b)
            d['geom']=writer.write(b.geom)
            d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
            return {'ok':True, 'Message': f"Retriewed Poligon: {len(l)}",
                'data':[d]}

    def delete(self, d:dict):

        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No Poligon with the id {d['id']}", "data":None}
        b:Rivers=l[0]
        b.delete()
        return {'ok':True, 'Message': f"Poligon deleted: 1",
                'data':[{'id':d["id"]}]}



    

