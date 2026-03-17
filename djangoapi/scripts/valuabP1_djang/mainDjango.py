"""
This files can be executed in the following way:

    python manage.py runscript script_without_extension

The scripts must be in the folder scripts

You can pass parameters to the scritp in the following way:+

    python manage.py runscript mainDjango --script-args nombreTabla funcion

All parameters are received in string format

"""
import sys
from scripts.valuabP1_djang.limit_polit.poligon_django import limite_politic_class
from scripts.valuabP1_djang.rivers.lines_django import Rivers_class

def run(*args):
    """python manage.py runscript scripts.valuabP1_djang.mainDjango --script-args limit_politico insert"""
    #print(__file__)
    #print("Hello script")

    if len(args) == 2:
        tableName = args[0]
        functionName = args[1]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["limit_politico", "rivers", "puntos_criticos"]:
        print("Error: The available table names are limit_politico, rivers, puntos_criticos")
        sys.exit(0)
    
    if functionName not in ["insert", "select", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, select, selectAsDict, delete or update")
        sys.exit(0)

    #diccionario para select y delete
    dict_id = {"id": 1} 

    #diccionarios de datos
    datos_poligono = {
        # FALLA 3: ST_Relate (Polígono que se come la mitad del distrito de "Amarilis" que cargaste antes)
        "id": 98, "nombre": "Polígono Invasor",  "provincia": "Test", "poblacion": 0, 
        "geom": "POLYGON((-76.22 -9.93, -76.20 -9.93, -76.20 -9.91, -76.22 -9.91, -76.22 -9.93))"
        # "id": 11,
        # "nombre": "Ambo",
        # "provincia": "Ambo",
        # "poblacion": 15000,
        # "geom": "POLYGON((-76.2000 -10.1500, -76.1500 -10.1500, -76.1500 -10.1000, -76.2000 -10.1000, -76.2000 -10.1500))"
    }
    datos_rio = {
        "id": 4,
        "nombre": "Río Huallaga",
        "descripcion": "Tramo Tingo María",
        "vertiente": "Atlántico",
        "provincia": "Leoncio Prado",
        "geom": "LINESTRING(390000 8970000, 391000 8972000, 392500 8975000, 394000 8978000, 395000 8980000)"
    }

    datos_punto = {
        "id": 1, 
        "nombre": "Ambo (Capital)", 
        "fuente": "ANA", 
        "fecha": 2025, 
        "riesgo": "Muy Alto", 
        "geom": "POINT(-76.20087 -10.13110)"
    }

    if tableName == "limit_politico":
        b = limite_politic_class()
        if functionName=="insert":
            print(b.insert(datos_poligono))
        elif functionName=="select":
            print(b.select(dict_id))
        elif functionName=="selectAsDict":
            print(b.select(dict_id, asDict=True))
        elif functionName=="update":
            print(b.update(datos_poligono))
        elif functionName=="delete":
            print(b.delete(dict_id))
    elif tableName=="rivers":
        b = Rivers_class()
        if functionName=="insert":
            print(b.insert(datos_rio))
        elif functionName=="select":
            print(b.select(dict_id))
        elif functionName=="selectAsDict":
            print(b.select(dict_id, asDict=True))
        elif functionName=="update":
            print(b.update(datos_rio))
        elif functionName=="delete":
            print(b.delete(dict_id))

if __name__ == "__main__":
    run()
