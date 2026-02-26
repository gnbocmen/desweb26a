import psycopg
from myLib import p1settings

def connect():
    conn = psycopg.connect(
        dbname=p1settings.POSTGRES_DB,
        user=p1settings.POSTGRES_USER,
        password=p1settings.POSTGRES_PASSWORD,
        host=p1settings.POSTGRES_HOST,
        port=p1settings.POSTGRES_PORT
    )
    return conn

def insert_linea():
    conn = connect()
    cur = conn.cursor()
    # Una línea necesita al menos 2 pares de coordenadas
    cons = """
        INSERT INTO rios (nombre, geom)
        VALUES (%s, ST_Transform(ST_GeomFromText(%s, 32718), 4326))
    """
    cur.execute(cons, ['Río Huallaga (Tramo Urbano)', 'LINESTRING(363197 8900999, 363644 8901327, 364481 8901843, 364784 8903006, 365398 8905356)'])
    conn.commit()
    cur.close()
    conn.close()
    print('Línea de río insertada')