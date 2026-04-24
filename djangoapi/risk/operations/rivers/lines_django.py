from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Rivers, Limit_politic

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Rivers_class():
    def insert(self, d:dict):
        # 1. Se quita el id del diccionario
        d.pop('id', None)

        # 2. Verificacion de EPSG
        g_raw = GEOSGeometry(d['geom'])

        #verificamos si no tiene SRID
        if g_raw.srid is None:
            return {'ok': False, 'message': 'Debe definir SRID', 'data': None}
        
        # 3.snap y transformacion de SRID
        
        # A) Obtener la geometría en Grados (4326) para validar y guardar
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

        # B) Obtener la geometría en UTM (32718) para calcular Área en metros reales
        query_utm = """
            SELECT ST_AsText(
                ST_Transform(
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s), 
                    32718
                )
            )
        """
        cur.execute(query_utm, [g_raw.wkt, g_raw.srid, ST_SNAP_PRECISION])
        g_utm = GEOSGeometry(cur.fetchone()[0], srid=32718)

                
        # 4. Validacion (Usando g_db que es 4326)
        if not g_db.valid:
            return {'ok': False, 'message': 'Invalid geometry', 'data': None}
        
        # 5. Validacion de intersección
        if d.get('id', -1) != 1:
            # Verificar que esté dentro de la región base (id=1)
            region = Limit_politic.objects.filter(id=1).first()
            if region and not g_db.within(region.geom):
                return {'ok': False, 'message': f'The geometry is not inside the region Huánuco (id=1). Coords calculadas: {g_db.wkt}', 'data': None}

            # Verificar que no se intersecte con otros límites (DE-9IM T********)
            query=""" 
                select id from risk_rivers 
                where ST_relate(
                    geom,
                    ST_GeomFromText(%s, 4326),
                    'T********')
            """
            cur.execute(query, [g_db.wkt])
            r=cur.fetchall()

            if len(r)>0:
                return {'ok': False, 'message':'The River intersects with the following rivers id', 'data': r}



        #6. Calculo del perimetro se transforma utm
        d['geom'] = g_db
        d['longitud'] = g_utm.length
        
        ##el ** desempaqueta el diccionario permitiendo que las claves sean nombres del parámetro y los valores en valores.
        b=Rivers(**d)
        b.save()

        #7. Respuesta
        #convertimos una instancia de modelo de django a diccionario
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'River inserted', 'data': [d]}

    def update(self, d:dict):
        # 1. Verificacion de EPSG
        g_raw = GEOSGeometry(d['geom'])

        if g_raw.srid is None:
            return {'ok': False, 'message': 'Debe definir SRID', 'data': None}
        
        # 2. Delegar Snap y Transformación a PostGIS
        cur = connection.cursor()

        # A) 4326 para Base de Datos
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

        # B) UTM 32718 para calcular Longitud en metros
        query_utm = """
            SELECT ST_AsText(
                ST_Transform(
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s), 
                    32718
                )
            )
        """
        cur.execute(query_utm, [g_raw.wkt, g_raw.srid, ST_SNAP_PRECISION])
        g_utm = GEOSGeometry(cur.fetchone()[0], srid=32718)

        # 3. Validación básica
        if not g_db.valid:
            return {'ok': False, 'message': 'Invalid geometry', 'data': None}
        
        # 4. Validación Espacial
        # Verificar que esté dentro de la región base (Huánuco id=1)
        region = Limit_politic.objects.filter(id=1).first()
        if region and not g_db.within(region.geom):
            return {'ok': False, 'message': f'The river is not inside the region Huánuco (id=1). Coords: {g_db.wkt}', 'data': None}

        # Verificar intersecciones con otros ríos (excluyendo a sí mismo)
        id_actual = d.get('id', -1)
        query = """ 
            SELECT id FROM risk_rivers 
            WHERE ST_relate(
                geom,
                ST_GeomFromText(%s, 4326),
                'T********'
            ) AND id != %s 
        """
        cur.execute(query, [g_db.wkt, id_actual])
        r = cur.fetchall()

        if len(r) > 0:
            return {'ok': False, 'message': 'The river intersects with others rivers id', 'data': r}

        # 5. Búsqueda y Actualización
        b = Rivers.objects.filter(id=d['id']).first()
        if not b:
            return {'ok': False, "message": f"No River was found with id {d['id']}", 'data': None}

        d['geom'] = g_db
        d['longitud'] = g_utm.length

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        
        # 6. Respuesta     
        
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': "Updated LineString",
                'data':[d]}

    def selectall(self):
        l = Rivers.objects.all()
        data = []
        writer = WKTWriter(precision=4)
        if len(l)==0:
            return {'ok':False, 'Message': f"No River exist",'data':[]}
        for b in l:
            d = model_to_dict(b)
            d['geom'] = writer.write(b.geom).decode('utf-8')
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
                
            data.append(d)
            
        return {'ok': True, 'Message': 'Data retrieved', 'data': data}

    def selectAsDict(self, d:dict):
    #filtrar por rango menor y mayor: Limit_politic.objects.filter(id__lt=3) o Limit_politic.objects.filter(id__gt=4)
    #por area creo tambien: Limit_politic.objects.filter(area__lt=100) o Limit_politic.objects.filter(area__gt=100)

        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4)
        d=model_to_dict(b)
        d['geom']=writer.write(b.geom).decode('utf-8')
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok':True, 'Message': f"Retriewed LineString: {len(l)}",
                'data':[d]}
        

    def selectAsTuples(self, d:dict):
    #create the geometry with geos
        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        
        b=l[0]
        writer = WKTWriter(precision=4).decode('utf-8')
        geom_wkt=writer.write(b.geom)
        data_creation_str = b.data_creation.strftime("%Y-%m-%d %H:%M:%S")

        tup= (b.id, b.nombre, b.descripcion, b.vertiente, b.longitud, b.provincia, geom_wkt, data_creation_str)
        return {'ok':True, 'Message': f"Retrieved River as Tuple: {len(l)}", 
                'data':[tup]}


    def delete(self, d:dict):

        f=Rivers.objects.filter(id=d['id'])
        l=list(f)
        if len(l)<1:
            return {"ok":False, "Message": f"No River with the id {d['id']}", "data":None}
        b:Rivers=l[0]
        b.delete()
        return {'ok':True, 'Message': f"LineString deleted: 1",
                'data':[{'id':d["id"]}]}



    

