from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.gis.geos import WKTWriter
from django.forms.models import model_to_dict
from django.db import connection

from risk.models import Limit_politic


from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class limite_politic_class():
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
                select id from risk_limit_politic 
                where ST_relate(
                    geom,
                    ST_GeomFromText(%s, 4326),
                    'T********')
                AND id != 1
            """
            cur.execute(query, [g_db.wkt])
            r=cur.fetchall()

            if len(r)>0:
                return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        # 6. Calculo de area y perimetro
        d['geom'] = g_db
        d['area'] = g_utm.area
        d['perimeter'] = g_utm.length
        
        b = Limit_politic(**d)
        b.save()
            
        #7. Respuesta
                
        #convertimos una instancia de modelo de django a diccionario
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Polígono inserted', 'data': [d]}

    def update(self, d:dict):

        # 1. Verificacion de EPSG
        g_raw = GEOSGeometry(d['geom'])

        #verificamos si no tiene SRID
        if g_raw.srid is None:
            return {'ok': False, 'message': 'Debe definir SRID', 'data': None}
                
        # 2.snap y transformacion de SRID

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
        
        
        # Validacion (Usando g_db que es 4326)
        if not g_db.valid:
            return {'ok': False, 'message': 'Invalid geometry', 'data': None}
        
        #3. Validacion de intersección
        if d.get('id', -1) != 1:
            # Verificar que esté dentro de la región base (id=1)
            region = Limit_politic.objects.filter(id=1).first()
            if region and not g_db.within(region.geom):
                return {'ok': False, 'message': 'The geometry is not inside the region Huánuco (id=1)', 'data': None}

            # Verificar que no se intersecte con otros límites (DE-9IM T********)

            query=""" 
                SELECT id FROM risk_limit_politic 
                WHERE ST_relate(
                    geom,
                    ST_GeomFromText(%s, 4326),
                    'T********')
                AND id != %s AND id != 1
            """
            cur.execute(query, [g_db.wkt, d['id']])
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

        #4. calculo de area
        d['geom']=g_db
        d['area']=g_utm.area
        d['perimeter']=g_utm.length

        for key, value in d.items():
            setattr(b, key, value)
        
        b.save()
        d=model_to_dict(b)
        d['geom']=g_db.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated Poligon: {len(l)}",
                'data':[d]}


    def selectallAsDicts(self):
        l = Limit_politic.objects.all()
        data = []
        writer = WKTWriter(precision=4)
        if len(l)==0:
            return {'ok':False, 'Message': f"No Building exist",'data':[]}
        for b in l:
            d = model_to_dict(b)
            d['geom'] = writer.write(b.geom)
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
                
            data.append(d)
            
        return {'ok': True, 'Message': f"Retrieved poligons: {len(l)}", 'data': data}

    def selectAsDict(self, d:dict):
    #filtrar por rango menor y mayor: Limit_politic.objects.filter(id__lt=3) o Limit_politic.objects.filter(id__gt=4)
    #por area creo tambien: Limit_politic.objects.filter(area__lt=100) o Limit_politic.objects.filter(area__gt=100)

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



    

