"""
This files can be executed in the following way:

    python manage.py runscript script_without_extension

The scripts must be in the folder scripts

You can pass parameters to the scritp in the following way:+

    python manage.py runscript mainDjango --script-args nombreTabla funcion

All parameters are received in string format

"""
import sys
#importar las clases
from scripts.valuabP1_djang.limit_polit.poligon_django import limite_politic_class
from scripts.valuabP1_djang.rivers.lines_django import Rivers_class
from scripts.valuabP1_djang.points_crit.pc_django import Puntos_class


##srid de la tabla 4326. de peru utm 32718. de españa 25830.

def run(*args):
    """python manage.py runscript scripts.valuabP1_djang.mainDjango --script-args limit_politico insert
    python manage.py runscript scripts.valuabP1_djang.mainDjango --script-args rivers insert
    python manage.py runscript scripts.valuabP1_djang.mainDjango --script-args points_crit insert
    """
    #print(__file__)
    #print("Hello script")

    if len(args) == 2:
        tableName = args[0]
        functionName = args[1]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["limit_politico", "rivers", "points_crit"]:
        print("Error: The available table names are limit_politico, rivers, points_crit")
        sys.exit(0)
    
    if functionName not in ["insert", "selectAsTuples", "selectallAsDicts", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, selectAsTuples, selectallAsDicts, selectAsDict, delete or update")
        sys.exit(0)

    #diccionario para select y delete
    dict_id = {"id": 5} 

    #diccionarios de datos
    datos_poligono = {
        # FALLA 3: ST_Relate (Polígono que se come la mitad del distrito de "Amarilis" que cargaste antes)
       "id": 98, "nombre": "Polígono Invasor",  "provincia": "Test", "poblacion": 0, 
        "geom": "POLYGON((-76.22 -9.93, -76.20 -9.93, -76.20 -9.91, -76.22 -9.91, -76.22 -9.93))"
        # "id": 12,
        # "nombre": "Región Huánuco",
        # "provincia": "11 Provincias",
        # "poblacion": 780000,
        # "geom": "POLYGON (())"
    }
    datos_rio = {
        # FALLA 3: ST_Relate (Se cruza como una "X" cortando exactamente por la mitad al "Río Huallaga Tramo Ambo" que insertaste antes)
        # "id": 95, "nombre": "Río Cruzado", "descripcion": "Choca con otro río", "vertiente": "N/A", "provincia": "Test", 
        # "geom": "LINESTRING(367000 8882000, 369500 8882000)"
        "id": 20, 
    "nombre": "Río Ebro", 
    "descripcion": "Tramo Bajo Huamalíes", 
    "vertiente": "Atlántico", 
    "longitud": 18500.5, 
    "provincia": "Huamalíes", 
    "geom": "LINESTRING(302000 8910000, 303000 8915000)"
    }

    datos_punto = {
        # FALLA : 
        #"id": 92, "nombre": "Fuerea", "fuente": "Test", "year": 2026, "nivel": "Bajo", 
        #"geom": "POINT(-50.000 10.000)"
         
    "nombre": "Deslizamiento  Carpish", 
    "fuente": "INDECI", 
    "nivel": "Muy Alto", 
    "year": 2025, 
    "geom": "POINT(-76.1012 -9.7185)"
    }

    if tableName == "limit_politico":
        b = limite_politic_class()
        if functionName=="insert":
            print(b.insert(datos_poligono))
        elif functionName=="selectAsDict":
            print(b.selectAsDict(dict_id))
        elif functionName=="selectAsTuples":
            print(b.selectAsTuples(dict_id))
        elif functionName=="update":
            print(b.update(datos_poligono))
        elif functionName=="delete":
            print(b.delete(dict_id))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())

    elif tableName=="rivers":
        b = Rivers_class()
        if functionName=="insert":
            print(b.insert(datos_rio))
        elif functionName=="selectAsDict":
            print(b.selectAsDict(dict_id))
        elif functionName=="selectAsTuples":
            print(b.selectAsTuples(dict_id))
        elif functionName=="update":
            print(b.update(datos_rio))
        elif functionName=="delete":
            print(b.delete(dict_id))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())

    
    elif tableName=="points_crit":
        b = Puntos_class()
        if functionName=="insert":
            print(b.insert(datos_punto))
        elif functionName=="selectAsDict":
            print(b.selectAsDict(dict_id))
        elif functionName=="selectAsTuples":
            print(b.selectAsTuples(dict_id))
        elif functionName=="update":
            print(b.update(datos_punto))
        elif functionName=="delete":
            print(b.delete(dict_id))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())


if __name__ == "__main__":
    run()
