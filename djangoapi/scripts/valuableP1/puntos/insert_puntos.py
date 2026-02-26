import psycopg
from valuableP1.myLib import p1Settings

def connect():
    conn = psycopg.connect(
        dbname=p1Settings.POSTGRES_DB,
        user=p1Settings.POSTGRES_USER,
        password=p1Settings.POSTGRES_PASSWORD,
        host=p1Settings.POSTGRES_HOST,
        port=p1Settings.POSTGRES_PORT
    )
    return conn

def insert_punto():
    conn = connect()
    cur = conn.cursor()
    # Insertamos un punto cerca al río Huallaga en Huánuco
    cons = """
        INSERT INTO puntos_criticos (nombre, fuente, fecha, geom)
        VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))
    """
    puntos = [
        ('Huayopampa', 'ANA', 2024, 'POINT(-76.23404 -9.91607)'),
        ('Ambo-mesapata', 'Gob. Regional', 2025, 'POINT(-76.178256 -10.122867)')]
    
    for p in puntos:
        cur.execute(cons, p)
    conn.commit()
    cur.close()
    conn.close()
    print('Puntos críticos insertados')