
import psycopg

from djangoapi.scripts.valuableP1.myLib import p1set_antiguo

def connect():
    conn= psycopg.connect(
        dbname=p1set_antiguo.POSTGRES_DB,
        user=p1set_antiguo.POSTGRES_USER,
        password=p1set_antiguo.POSTGRES_PASSWORD,
        host=p1set_antiguo.POSTGRES_HOST,
        port=p1set_antiguo.POSTGRES_PORT
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
