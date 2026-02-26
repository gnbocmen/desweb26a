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
    def insert(self):
        cons = """
        INSERT INTO b1.limit_politico 
            (nombre, departamento, provincia, poblacion, geom)
        VALUES
            (%s, %s, %s, %s, ST_GeomFromText(%s, %s))
        RETURNING id
        """
        poligono = "POLYGON((-77.2917 -8.4836, -75.9927 -8.3194, -75.6607 -9.4335, -74.6224 -8.5445, -74.5198 -8.7820, -74.8709 -9.8787, -75.9921 -10.5052, -76.7636 -10.4916, -77.0461 -9.6385, -77.2917 -8.4836))"
        
        self.cur.execute(cons, [
            'Región Huánuco', 'Huánuco', 'Huánuco', 854234, 
            poligono, EPSG_CODE
        ])
        self.conn.commit()
        l=self.cur.fetchall()
        print(l)
        print(l[0][0])
        self.disconnect()
        print("Inserted")

    def select(self, asDict=False):
        if asDict:
            self.cur = self.conn.cursor(row_factory=dict_row)
        
        cons = """
        SELECT 
            id, nombre, poblacion, st_astext(geom) 
        FROM 
            b1.limit_politico 
        WHERE 
            id = %s
        """
        self.cur.execute(cons, [1])
        l=self.cur.fetchall()
        print(l)
        print('Primera Linea:')
        print(l[0])
        self.disconnect()
        print("Selected")

    def delete(self):
        cons="""
            DELETE FROM
                b1.limit_politico 
            WHERE
                id=%s
            """
        valuesList=[4]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Deleted")

    def update(self):
        cons = """
        UPDATE 
            b1.limit_politico 
        SET 
            (nombre, departamento, provincia, poblacion, geom) = 
                ROW(%s, %s, %s, %s, ST_GeomFromText(%s, %s))
        WHERE 
            id = %s
        """
        poligono_nuevo = "POLYGON((-76.515 -10.1536, -76.144 -9.9769, -76.03544 -10.1029, -76.03679 -10.5152, -76.51758 -10.30803, -76.515 -10.1536))" 
        
        valuesList = [
            'Provincia Ambo', 'Huánuco', 'Ambo', 50880, 
            poligono_nuevo, EPSG_CODE, 1
        ]

        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Updated")


