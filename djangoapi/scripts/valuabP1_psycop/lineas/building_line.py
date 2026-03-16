from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE

class buildings_line():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()
    
    def validate_data(self, data_dict):
        self.cur.execute("SELECT ST_ISVALID(ST_GeomFromText(%s, 32718))", [data_dict['geom']])
        is_valid = self.cur.fetchall()[0][0]
        if not is_valid:
            return False, "Geometria inválida"
        query = """
        SELECT ST_WITHIN(ST_SnapToGrid(ST_Transform(ST_GeomFromText(%s, 32718), %s), 0.0001), (SELECT geom FROM b1.limit_politico WHERE id = 1))
        """
        self.cur.execute(query, [data_dict['geom'], EPSG_CODE])
        is_within = self.cur.fetchall()[0][0]
        if not is_within:
            return False, "Geometria no esta dentro de la frontera politica"
        query2 = """
        SELECT EXISTS (
            SELECT 1 FROM b1.rios WHERE ID != %s 
            AND ST_RELATE(geom, ST_SnapToGrid(ST_Transform(ST_GeomFromText(%s, 32718), %s), 0.0001), 'T********')
        )
        """
        self.cur.execute(query2, [data_dict.get('id', -1), data_dict['geom'], EPSG_CODE])
        is_relate = self.cur.fetchall()[0][0]
        if is_relate:
            return False, "Geometria se interseca con otro rio"
        return True, "valido"

    def insert(self, data_dict):
        try:
            es_valido, mensaje = self.validate_data(data_dict)
            if not es_valido:
                self.disconnect()
                return {"ok": False, "message": mensaje, "data": None}

            cons="""
            INSERT INTO b1.rios 
                (nombre, descripcion, vertiente, provincia, geom)
            VALUES
                (%s, %s, %s, %s, ST_SnapToGrid(ST_Transform(ST_GeomFromText(%s, 32718), %s), 0.0001))
            RETURNING id
            """
            self.cur.execute(cons,
                        [data_dict['nombre'], data_dict['descripcion'], data_dict['vertiente'], data_dict['provincia'], 
                        data_dict['geom'], EPSG_CODE])
                        
            self.conn.commit()
            l=self.cur.fetchall()[0][0]
            self.disconnect()
            return {"ok": True, "message": "Data inserted", "data": [{"id": l}]}
        
        except Exception as e:
            self.disconnect()
            return {"ok": False, "message": f"Error inserting data: {str(e)}", "data": None}

    def select(self, data_dict, asDict=False):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        try:
            cons="""
            SELECT 
                id, nombre, descripcion, vertiente, provincia,  ST_AsText(ST_SnapToGrid(geom, 0.0001)) as geom
            FROM 
                b1.rios 
            WHERE
                id=%s
            """
            self.cur.execute(cons, [data_dict['id']])
            l=self.cur.fetchall()
            self.disconnect()
            return {"ok": True, "message": "Data selected", "data": l}
        
        except Exception as e:
            self.disconnect()
            return {"ok": False, "message": f"Error selecting data: {str(e)}", "data": None}

    def delete(self, data_dict):
        try:
            cons="""
                DELETE FROM
                    b1.rios 
                WHERE
                    id=%s
                """
            # As there are 5 %s, you need a list with 5 values: 
            #   [description, area, the_geom_wkt, the_epsg_code, 
            #           the_id_to_select_the_row]
            
            self.cur.execute(cons, [data_dict['id']])
            self.conn.commit()
            self.disconnect()
            return {"ok": True, "message": "Data deleted", "data": data_dict['id']}

        except Exception as e:            
            self.disconnect()
            return {"ok": False, "message": f"Error deleting data: {str(e)}", "data": None}

    def update(self, data_dict):
        try:
            es_valido, mensaje = self.validate_data(data_dict)
            if not es_valido:
                self.disconnect()
                return {"ok": False, "message": mensaje, "data": None}

            cons="""
                UPDATE
                    b1.rios 
                SET 
                    (nombre, descripcion, vertiente, provincia, geom) = 
                        ROW(%s, %s, %s, %s, ST_SnapToGrid(ST_Transform(ST_GeomFromText(%s, 32718), %s), 0.0001))
                WHERE
                    id=%s
                """

            self.cur.execute(cons, [data_dict['nombre'], data_dict['descripcion'], data_dict['vertiente'], 
                                    data_dict['provincia'], data_dict['geom'], EPSG_CODE, data_dict['id']])
            
            self.conn.commit()
            self.disconnect()
            return {"ok": True, "message": "Data updated", "data": data_dict['id']}
        
        except Exception as e:
            self.disconnect()
            return {"ok": False, "message": f"Error updating data: {str(e)}", "data": None}




            
