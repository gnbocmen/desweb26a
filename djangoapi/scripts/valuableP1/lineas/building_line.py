from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class buildings_line():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()
    def insert(self):
        cons="""
        INSERT INTO b1.rios 
            (nombre, descripcion, vertiente, provincia, geom)
        VALUES
            (%s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 32718), %s))
        RETURNING id
        """
        self.cur.execute(cons,
                    ['Río Huallaga I', 'Tramo Urbano', 'Amazónico', 'Huánuco', 
                     'LINESTRING(363197 8900999, 363644 8901327, 364481 8901843, 364784 8903006, 365398 8905356)', 
                     EPSG_CODE])
        self.conn.commit()
        l=self.cur.fetchall()
        #print(cur.fetchall()[0][0]) <-- ERROR. YOU ONLY CAN FECTH THE RESULTS ONCE
        print(l)
        print(l[0][0])
        self.disconnect()
        print("Inserted")
    def select(self, asDict=True):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        cons="""
        SELECT 
            id, nombre,  st_astext(geom)
        FROM 
            b1.rios 
        WHERE
            id=%s
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
                b1.rios 
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=[2]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.disconnect()
        print("Deleted")

    def update(self):
        cons="""
            UPDATE
                b1.rios 
            SET 
                (nombre, geom) = ROW(%s, ST_Transform(ST_GeomFromText(%s, 32718), %s))    

            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=['Río Huallaga (Tramo II)', 
                     'LINESTRING(363197 8900999, 363644 8901327, 364481 8901843, 364784 8903006, 365398 8905356)',
                     EPSG_CODE, 4]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.disconnect()
        print("Updated")




            
