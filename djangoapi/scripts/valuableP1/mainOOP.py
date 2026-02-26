import sys
#from puntos.insert_puntos import insert_punto
from poligonos.building_polig import buildings_polig    
from lineas.building_line import buildings_line
from puntos.building_punto import buildings_point
#from poligonos.insert_polyg import insert_poligono


def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["puntos_criticos", "rios", "limit_politico"]:
        print("Error: The available table names are puntos_criticos, rios, limit_politico")
        sys.exit(0)
    
    if functionName not in ["insert", "select", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, select, delete or update")
        sys.exit(0)

    if tableName == "rios":
        b=buildings_line()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="selectAsDict":
            b.select(asDict=True)
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()
    elif tableName=="limit_politico":
        b=buildings_polig()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="selectAsDict":
            b.select(asDict=True)
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()

    elif tableName=="puntos_criticos":
        b=buildings_point()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="selectAsDict":
            b.select(asDict=True)
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()


if __name__ == "__main__":
    main()

