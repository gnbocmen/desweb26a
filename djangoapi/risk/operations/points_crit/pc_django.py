from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Points_crit
from scripts.valuabP1_djang.myLib import p1settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Puntos_class():
    def insert(self, d:dict):
        #we first get the snapped wkb format for the geometry:
        cur=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, 4326),%s)"
        cur.execute(query, [d['geom'], ST_SNAP_PRECISION])
        snapped_wkb_geometry=cur.fetchall()[0][0]

        #print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

        #now we can check if it is valid as before:
        #srid de la tabla 4326. 
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
            return {'ok': False, 'message':'The point is not inside the region Huánuco (id=1)', 'data': None}
        
        
        d['geom']=g
        ##el ** desempaqueta el diccionario permitiendo que las claves sean nombres del parámetro y los valores en valores.
        b=Points_crit(**d)
        b.save()
        #convertimos una instancia de modelo de django a diccionario
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
        
        #verificamos que este dentro de la región:
        query_within = "SELECT ST_Within(%s::geometry, (SELECT geom FROM risk_limit_politic WHERE id = 1))"
        cur.execute(query_within, [snapped_wkb_geometry])
        r=cur.fetchall()
        if r and r[0][0] is False:
            return {'ok': False, 'message':'The point is not inside the region Huánuco (id=1)', 'data': None}

        #create the geometry with geos
        f=Points_crit.objects.filter(id=d['id'])
        l=list(f)
        if len(l)>0:
            b:Points_crit=l[0]
        else:
            return {'ok':False, "message": f"No Point was found with id {d['id']}", 'data':None}

        
        d['geom']=g

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated Poligon: {len(l)}",
                'data':[d]}


    def selectAsDict(self, d:dict):
    #filtrar por rango menor y mayor: Limit_politic.objects.filter(id__lt=3) o Limit_politic.objects.filter(id__gt=4)
    #por area creo tambien: Limit_politic.objects.filter(area__lt=100) o Limit_politic.objects.filter(area__gt=100)

        f=Points_crit.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No point with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        d=model_to_dict(b)
        d['geom']=writer.write(b.geom)
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok':True, 'Message': f"Retriewed Point: {len(l)}",
                'data':[d]}
        
    def selectallAsDicts(self):
        l = Points_crit.objects.all()
        data = []
        writer = WKTWriter(precision=4)
        
        for b in l:
            d = model_to_dict(b)
            d['geom'] = writer.write(b.geom)
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
                
            data.append(d)
            
        return {'ok': True, 'Message': 'Data retrieved', 'data': data}

    def selectAsTuples(self, d:dict):
    #create the geometry with geos
        f=Points_crit.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No Point with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        geom_wkt=writer.write(b.geom)
        data_creation_str = b.data_creation.strftime("%Y-%m-%d %H:%M:%S")

        tup= (b.id, b.nombre, b.fuente, b.nivel, b.year, geom_wkt, data_creation_str)
        return {'ok':True, 'Message': f"Retrieved Point as Tuple: {len(l)}", 
                'data':[tup]}

    def delete(self, d:dict):

        f=Points_crit.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No Point with the id {d['id']}", "data":None}
        b:Points_crit=l[0]
        b.delete()
        return {'ok':True, 'Message': f"Point deleted: 1",
                'data':[{'id':d["id"]}]}



    

