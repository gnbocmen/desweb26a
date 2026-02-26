
import psycopg

from myLib import p1settings

def connect():
    conn= psycopg.connect(
        dbname=p1settings.POSTGRES_DB,
        user=p1settings.POSTGRES_USER,
        password=p1settings.POSTGRES_PASSWORD,
        host=p1settings.POSTGRES_HOST,
        port=p1settings.POSTGRES_PORT
    )

    print('Conectado')
    return conn

def insert ():
    conn = connect()
    cur = conn.cursor()
    cons = """
        INSERT INTO d.buildings 
            (description, area, geom)
        VALUES 
            (%s,%s,st_geomfromtext(%s,25830))
        RETURNING id
        """
    cur.execute(cons,['Edificio A', 
                      100,
                      'POLYGON((0 0, 0 100, 100 100, 100 0, 0 0))'])
    conn.commit()
    cur.close()
    conn.close()
    print('Insertado')
