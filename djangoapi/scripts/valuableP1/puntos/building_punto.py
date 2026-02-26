from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE

class buildings_point():
    def __init__(self):
        self.conn = connect()
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self):
        cons = """
        INSERT INTO b1.puntos_criticos 
            (nombre, fuente, fecha, riesgo, geom)
        VALUES
            (%s, %s, %s, %s, ST_GeomFromText(%s, %s))
        RETURNING id
        """
        # EPSG_CODE lo pasamos como parámetro para 4326
        self.cur.execute(cons, [
            'Huayopampa', 'ANA', 2024, 'Alto', 
            'POINT(-76.23404 -9.91607)', EPSG_CODE
        ])
        self.conn.commit()
        l = self.cur.fetchall()
        print(l)
        print(l[0][0])
        self.disconnect()
        print("Inserted")

    def select(self, asDict=False):
        if asDict:
            self.cur = self.conn.cursor(row_factory=dict_row)
        
        cons = """
        SELECT 
            id, nombre, fuente, fecha, riesgo, st_astext(geom)
        FROM 
            b1.puntos_criticos 
        WHERE 
            id = %s
        """
        self.cur.execute(cons, [1]) 
        l = self.cur.fetchall()
        print(l)
        print('Primera Linea:')
        print(l[0])
        self.disconnect()
        print("Selected")

    def delete(self):
        cons = """
            DELETE FROM 
                b1.puntos_criticos 
            WHERE 
                id = %s
            """
        valuesList=[3]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Deleted")

    def update(self):
        cons = """
        UPDATE 
            b1.puntos_criticos 
        SET 
            (nombre, fuente, fecha, riesgo, geom) = 
                ROW(%s, %s, %s, %s, ST_GeomFromText(%s, %s))
        WHERE 
            id = %s
        """
        valuesList = [
            'Ambo-mesapata', 'Gob. Regional', 2025, 'Alto', 
            'POINT(-76.178256 -10.122867)', EPSG_CODE, 2
        ]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Updated")

            
