import sys

from poligonos.building_polig import buildings_polig    
from lineas.building_line import buildings_line
from puntos.building_punto import buildings_point



datos_nuevo_punto = {
        "id": 3,
        "nombre": "Rio Huallaga Ambo",
        "fuente": "ANA",
        "fecha": 2025,
        "riesgo": "Alto",
        "geom": "POINT(-76.19989 -10.13202)"
    }

datos_nueva_linea = {
    "id": 3,
    "nombre": "Río Huallaga Tingo María",
    "descripcion": "Tramo Ciudad de Tingo María",
    "vertiente": "Amazónico",
    "provincia": "Leoncio Prado",
    "geom": 'LINESTRING(404391.59 8937586.72, 392599.98 8955145.77, 393954.33 8957740.35, 392312.94 8966464.28, '
    '389248.90 8969990.44, 389970.10 8972605.58, 390347.70 8981587.13, 388109.39 8987323.85)'
}


datos_nuevo_poligono = {
    "id": 5,
    "nombre": "Provincia",
    "departamento": "Huánuco",
    "provincia": "Huánuco",
    "poblacion": 318535,
    "geom": 'SRID=4326; POLYGON((-76.511238 -10.154535, -76.5174297 -10.1869513, -76.602283 -10.090962, -76.477371 -9.747242, '
    '-76.35468548 -9.5415351, -76.14317648 -9.46988235, -75.9577062 -9.4935442, -75.77123010 -9.7880332, -75.819989 -9.8304533, '
    '-76.0501698 -9.823050, -76.1355214 -9.98829097, -76.14459528 -9.9769758, -76.511238 -10.154535))'
}

#Id para funciones select y delete
diccionario_id = {'id': 5}

def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]     
    else:
        print("Error: You must give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["puntos_criticos", "rios", "limit_politico"]:
        print("Error: The available table names are puntos_criticos, rios, limit_politico")
        sys.exit(0)
    
    if functionName not in ["insert", "selectAsTuple", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, selectAsTuple, selectAsDict, update or delete")
        sys.exit(0)

    

    if tableName == "rios":
        b=buildings_line()
        if functionName=="insert":
            print(b.insert(datos_nueva_linea))
        elif functionName=="selectAsTuple":
            print(b.select(diccionario_id))
        elif functionName=="selectAsDict":
            print(b.select(diccionario_id, asDict=True))
        elif functionName=="update":
            print(b.update(datos_nueva_linea))
        elif functionName=="delete":
            print(b.delete(diccionario_id))

    elif tableName=="limit_politico":
        b=buildings_polig()
        if functionName=="insert":
            print(b.insert(datos_nuevo_poligono))
        elif functionName=="selectAsTuple":
            print(b.select(diccionario_id))
        elif functionName=="selectAsDict":
            print(b.select(diccionario_id, asDict=True))
        elif functionName=="update":
            print(b.update(datos_nuevo_poligono))
        elif functionName=="delete":
            print(b.delete(diccionario_id))

    elif tableName=="puntos_criticos":
        b=buildings_point()
        if functionName=="insert":
            print(b.insert(datos_nuevo_punto))
        elif functionName=="selectAsTuple":
            print(b.select(diccionario_id))
        elif functionName=="selectAsDict":
            print(b.select(diccionario_id, asDict=True))
        elif functionName=="update":
            print(b.update(datos_nuevo_punto))
        elif functionName=="delete":
            print(b.delete(diccionario_id))


if __name__ == "__main__":
    main()

