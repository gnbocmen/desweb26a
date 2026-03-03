from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class buildings_polig():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self, data_dict):
        try:
            cons = """
            INSERT INTO b1.limit_politico 
                (nombre, departamento, provincia, poblacion, geom)
            VALUES
                (%s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, %s), 0.0001))
            RETURNING id
            """        
        
            self.cur.execute(cons, [
                data_dict['nombre'], data_dict['departamento'], data_dict['provincia'], data_dict['poblacion'], 
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
            self.cur = self.conn.cursor(row_factory=dict_row)
        
        try:
            cons = """
            SELECT 
                id, nombre, poblacion, ST_AsText(ST_SnapToGrid(geom, 0.0001)) as geom
            FROM 
                b1.limit_politico 
            WHERE 
                id = %s
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
                    b1.limit_politico 
                WHERE
                    id=%s
                """
            self.cur.execute(cons, [data_dict['id']])
            self.conn.commit()
            self.disconnect()
            return {"ok": True, "message": "Data deleted", "data": data_dict['id']}

        except Exception as e:
            self.disconnect()
            return {"ok": False, "message": f"Error deleting data: {str(e)}", "data": None}

    def update(self, data_dict):
        try:
            cons = """
            UPDATE 
                b1.limit_politico 
            SET 
                (nombre, departamento, provincia, poblacion, geom) = 
                    ROW(%s, %s, %s, %s, ST_GeomFromText(%s, %s))
            WHERE 
                id = %s
            """

            self.cur.execute(cons, [
                data_dict['nombre'], data_dict['departamento'], data_dict['provincia'], data_dict['poblacion'], 
                data_dict['geom'], EPSG_CODE, data_dict['id']])

            self.conn.commit()
            self.disconnect()
            return {"ok": True, "message": "Data updated", "data": data_dict['id']}
        
        except Exception as e:
            self.disconnect()
            return {"ok": False, "message": f"Error updating data: {str(e)}", "data": None}

