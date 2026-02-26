import psycopg
from djangoapi.scripts.valuableP1.myLib import p1set_antiguo

def connect():
    conn = psycopg.connect(
        dbname=p1set_antiguo.POSTGRES_DB,
        user=p1set_antiguo.POSTGRES_USER,
        password=p1set_antiguo.POSTGRES_PASSWORD,
        host=p1set_antiguo.POSTGRES_HOST,
        port=p1set_antiguo.POSTGRES_PORT
    )
    return conn

def insert_poligono():
    conn = connect()
    cur = conn.cursor()
    cons = """
        INSERT INTO limit_politico (nombre, geom)
        VALUES (%s, ST_GeomFromText(%s, 4326))
    """
    cur.execute(cons, ['Bosquejo Region Huánuco', 'POLYGON((-77.291789 -8.483670, -75.992772 -8.319429, -75.660775 -9.433500, -74.622435 -8.544538, -74.519826 -8.782046, -74.870905 -9.878778, -75.992172 -10.505219, -76.763600 -10.491693, -77.046163 -9.638508, -77.291789 -8.483670))'])
    conn.commit()
    cur.close()
    conn.close()
    print('Polígono de límite político insertado')