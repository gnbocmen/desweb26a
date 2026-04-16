from django.http import JsonResponse
from django.views import View

#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks
from buildings.models import Buildings, Owners, BuildingsOwners
from buildings.serializers import BuildingsSerializer, OwnersSerializer, BuildingsOwnersSerializer
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION, MAX_NUMBER_OF_RETRIEVED_ROWS
from core.myLib.baseDjangoView import BaseDjangoView


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

class Risk(View):
    def post(self, request):
        d=request.POST.dict()
        
        return JsonResponse({"ok":True,"message": "Datos Recibidos", "data":[request.POST.dict()]},status=200)