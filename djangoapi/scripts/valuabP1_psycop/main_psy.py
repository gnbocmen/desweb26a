import sys

from poligonos.building_polig import buildings_polig    
from lineas.building_line import buildings_line
from puntos.building_punto import buildings_point



datos_nuevo_punto = {
    # FALLA 2: ST_Within (Extremadamente fuera. Coordenadas de la estación Benimaclet en Valencia)
        "id": 91, "nombre": "Falla Dentro 2", "fuente": "Test", "fecha": 2026, "riesgo": "Bajo", 
        "geom": "POINT(-0.3621 39.4802)"
        # "id": 11, 
        # "nombre": "Uchucyacu", 
        # "fuente": "INGEMMET", 
        # "fecha": 2025, 
        # "riesgo": "Muy Alto", 
        # "geom": "POINT(-76.31916 -10.26356)"
    }

datos_nueva_linea = {
        # FALLA 3: ST_Relate (Se cruza como una "X" cortando exactamente por la mitad al "Río Huallaga Tramo Ambo" que insertaste antes)
        "id": 10, "nombre": "Río Cruzado", "descripcion": "Choca con otro río", "vertiente": "N/A", "provincia": "Test", 
        "geom": "LINESTRING(367000 8882000, 369500 8882000)"
        # "id": 4,
        # "nombre": "Río Huallaga",
        # "descripcion": "Tramo de Santa María del Valle",
        # "vertiente": "Amazónico",
        # "provincia": "Huánuco",
        # "geom": "LINESTRING(365398 8905356, 370039.10868 8907829.69582, 373017.805239 8912749.058326, 377576.1136155 8915908.2819537, 377576.113615 8915908.28195)"
    }


datos_nuevo_poligono = {
    # FALLA 3: ST_Relate (Polígono que se come la mitad del distrito de "Amarilis" que cargaste antes)
        "id": 98, "nombre": "Polígono Interseca", "departamento": "Test", "provincia": "Test", "poblacion": 0, 
        "geom": "POLYGON((-76.22 -9.93, -76.20 -9.93, -76.20 -9.91, -76.22 -9.91, -76.22 -9.93))"
    # "id": 11,
    #     "nombre": "Ambo",
    #     "departamento": "Huánuco",
    #     "provincia": "Ambo",
    #     "poblacion": 15000,
    #     "geom": "POLYGON((-76.2000 -10.1500, -76.1500 -10.1500, -76.1500 -10.1000, -76.2000 -10.1000, -76.2000 -10.1500))"
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

