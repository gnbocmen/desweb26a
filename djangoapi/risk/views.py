from django.http import JsonResponse
from django.views import View

#My imports
# from core.myLib.geometryTools import WkbConversor, GeometryChecks
# from buildings.models import Buildings, Owners, BuildingsOwners
# from buildings.serializers import BuildingsSerializer, OwnersSerializer, BuildingsOwnersSerializer
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION, MAX_NUMBER_OF_RETRIEVED_ROWS
from core.myLib.baseDjangoView import BaseDjangoView


#Funciones
from risk.operations.limit_polit.poligon_django import limite_politic_class
from risk.operations.rivers.lines_django import Rivers_class
from risk.operations.points_crit.pc_django import Puntos_class



class Point_view(BaseDjangoView):
    #GET OPERATIONS
    def selectone(self, id):
        operaciones=Puntos_class()
        r = operaciones.selectAsDict({'id': id})
        
        return JsonResponse(r)

    def selectall(self):
        operaciones = Puntos_class()
        # Llamar al método selectall de tu clase
        r = operaciones.selectall()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()
        # 2. Instanciar y ejecutar
        operaciones = Puntos_class()
        r = operaciones.insert(d)
        return JsonResponse(r)
        
    def update(self, request, id):
        d = request.POST.dict()
        # Se agrega el id de la URL al diccionario 
        d['id'] = id 
        
        operaciones = Puntos_class()
        r = operaciones.update(d)
        return JsonResponse(r)
    
    def delete(self, id):
        d = {'id': id}
        operaciones = Puntos_class()
        r = operaciones.delete(d)
        return JsonResponse(r)


class River_view(BaseDjangoView):
    #GET OPERATIONS
    def selectone(self, id):
        operaciones=Rivers_class()
        r = operaciones.selectAsDict({'id': id})
        
        return JsonResponse(r)

    def selectall(self):
        operaciones = Rivers_class()
        # Llamar al método selectall de tu clase
        r = operaciones.selectall()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()
        # 2. Instanciar y ejecutar
        operaciones = Rivers_class()
        r = operaciones.insert(d)
        return JsonResponse(r)
        
    def update(self, request, id):
        d = request.POST.dict()
        # Se agrega el id de la URL al diccionario 
        d['id'] = id 
        
        operaciones = Rivers_class()
        r = operaciones.update(d)
        return JsonResponse(r)
    
    def delete(self, id):
        d = {'id': id}
        operaciones = Rivers_class()
        r = operaciones.delete(d)
        return JsonResponse(r)

class Polig_view(BaseDjangoView):
    #GET OPERATIONS
    def selectone(self, id):
        operaciones=limite_politic_class()
        r = operaciones.selectAsDict({'id': id})
        
        return JsonResponse(r)

    def selectall(self):
        operaciones = limite_politic_class()
        # Llamar al método selectall de tu clase
        r = operaciones.selectall()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()
        # 2. Instanciar y ejecutar
        operaciones = limite_politic_class()
        r = operaciones.insert(d)
        return JsonResponse(r)
        
    def update(self, request, id):
        d = request.POST.dict()
        # Se agrega el id de la URL al diccionario 
        d['id'] = id 
        
        operaciones = limite_politic_class()
        r = operaciones.update(d)
        return JsonResponse(r)
    
    def delete(self, id):
        d = {'id': id}
        operaciones = limite_politic_class()
        r = operaciones.delete(d)
        return JsonResponse(r)

#my code
#from risk.operations.classeee import funcion_insert_etc

"""
Código	Nombre	Uso típico
200	OK	Petición exitosa (valor por defecto).
201	Created	Se ha creado un recurso (ej. un nuevo usuario).
400	Bad Request	Datos enviados inválidos o mal formateados.
401	Unauthorized	El usuario no está autenticado.
403	Forbidden	Autenticado, pero sin permisos para esa acción.
404	Not Found	El recurso solicitado no existe.
500	Internal Server Error	Error inesperado en tu código Python.

"""


class HelloRisk(View):
    def get(self, request):
        
        return JsonResponse({"ok":True,"message": "Core. Hello world. Method: GET", "data":[request.GET.dict()]},status=200)
    def post(self, request):
        
        return JsonResponse({"ok":True,"message": "Core. Hello world. Method: POST", "data":[request.POST.dict()]},status=200)


# class PuntosView(BaseDjangoView):
#     def insert(self, request):
#         d = request.POST.dict()      # 1. Sacas el diccionario de internet
#         clase_puntos = PuntosClass() # 2. Llamas a tu clase trabajadora
#         r = clase_puntos.insert(d)   # 3. Le pasas el diccionario
#         return JsonResponse(r)       # 4. Devuelves el resultado a Postman

#     def selectall(self):
#         clase_puntos = PuntosClass()
#         r = clase_puntos.selectallAsDicts() 
#         return JsonResponse(r)
        
    # (Y así harías con update, delete, y selectone)

# class RiosView(BaseDjangoView):
#     # Harías exactamente lo mismo, pero llamando a RiosClass()
#     ...

# class LimitesView(BaseDjangoView):
#     # Harías exactamente lo mismo, pero llamando a LimitesClass()
#     ...

    

# class Risk(View):
#     def post(self, request):
#         d=request.POST.dict()
        
#         return JsonResponse({"ok":True,"message": "Datos Recibidos", "data":[request.POST.dict()]},status=200)