from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Points_crit, Limit_politic

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Puntos_class():
    def insert(self, d:dict):

        # 1. Forzar un Insert limpio
        d.pop('id', None)

        # 2. Verificacion de EPSG explícito
        g_raw = GEOSGeometry(d['geom'])

        if g_raw.srid is None:
            return {'ok': False, 'message': 'Debe definir SRID', 'data': None}
        
        # 3. Delegar Snap y Transformación a PostGIS (Solo 4326)
        cur = connection.cursor()
        query_4326 = """
            SELECT ST_AsText(
                ST_Transform(
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s), 
                    4326
                )
            )
        """
        cur.execute(query_4326, [g_raw.wkt, g_raw.srid, ST_SNAP_PRECISION])
        g_db = GEOSGeometry(cur.fetchone()[0], srid=4326)

        # 4. Validación básica
        if not g_db.valid:
            return {'ok': False, 'message': 'Invalid geometry', 'data': None}
        
        # 5. Validación Espacial (Dentro de Huánuco)
        region = Limit_politic.objects.filter(id=1).first()
        if region and not g_db.within(region.geom):
            return {'ok': False, 'message': f'The point is not inside the region Huánuco (id=1). Coords: {g_db.wkt}', 'data': None}

        # 6. Guardado
        d['geom'] = g_db
        b = Points_crit(**d)
        b.save()
        
        # 7. Respuesta
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Polígono inserted', 'data': [d]}


    def update(self, d:dict):
        # 1. Verificacion de EPSG
        g_raw = GEOSGeometry(d['geom'])

        if g_raw.srid is None:
            return {'ok': False, 'message': 'Debe definir SRID', 'data': None}
        
        # 2. Delegar Snap y Transformación a PostGIS
        cur = connection.cursor()
        query_4326 = """
            SELECT ST_AsText(
                ST_Transform(
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s), 
                    4326
                )
            )
        """
        cur.execute(query_4326, [g_raw.wkt, g_raw.srid, ST_SNAP_PRECISION])
        g_db = GEOSGeometry(cur.fetchone()[0], srid=4326)

        # 3. Validación básica
        if not g_db.valid:
            return {'ok': False, 'message': 'Invalid geometry', 'data': None}
        
        # 4. Validación Espacial
        region = Limit_politic.objects.filter(id=1).first()
        if region and not g_db.within(region.geom):
            return {'ok': False, 'message': f'The point is not inside the region Huánuco (id=1). Coords: {g_db.wkt}', 'data': None}

        # 5. Búsqueda y Actualización
        b = Points_crit.objects.filter(id=d['id']).first()
        if not b:
            return {'ok': False, "message": f"No Point was found with id {d['id']}", 'data': None}

        
        d['geom'] = g_db

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': "Updated Point",
                'data':[d]}


    def selectall(self):
        l = Puntos_class.objects.all()
        data = []
        writer = WKTWriter(precision=4)
        if len(l)==0:
            return {'ok':False, 'Message': f"No Point exist",'data':[]}
        for b in l:
            d = model_to_dict(b)
            d['geom'] = writer.write(b.geom).decode('utf-8')
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
                
            data.append(d)
            
        return {'ok': True, 'Message': f"Retrieved poligons: {len(l)}", 'data': data}
    
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
        d['geom']=writer.write(b.geom).decode('utf-8')
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok':True, 'Message': f"Retriewed Point: {len(l)}",
                'data':[d]}
        
   
    def selectAsTuples(self, d:dict):
    #create the geometry with geos
        f=Points_crit.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No Point with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        geom_wkt=writer.write(b.geom).decode('utf-8')
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



    

