
# from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from apps.afiliados.models import Afiliado
from apps.alquileres.models import Encargado
from .models import Persona  # Supongamos que tienes un modelo Persona
from apps.personas.models import Rol
from selectable.base import ModelLookup, LookupBase
from selectable.registry import registry
from unidecode import unidecode


class RolLookup(ModelLookup):
    model = Rol
    search_fields = ('persona__dni__icontains', 'persona__nombre__icontains','persona__apellido__icontains')
    
    def get_query(self, request, term):
        queryset = super().get_query(request, term)
        queryset = queryset.filter(hasta__isnull=True)
        return queryset.order_by('persona__dni')[:5] 

    def format_item_display(self, item):
        # Utiliza unidecode para eliminar las tildes
        nombre_sin_tildes = unidecode(item.persona.nombre)
        apellido_sin_tildes = unidecode(item.persona.apellido)
        return f'{nombre_sin_tildes} {apellido_sin_tildes} ({item.persona.dni})'


registry.register(RolLookup)

class EncargadoLookup(ModelLookup):
    model = Encargado
    search_fields = ('persona__dni__icontains', 'persona__nombre__icontains','persona__apellido__icontains')
    
    def get_query(self, request, term):
        queryset = super().get_query(request, term)
        # Filtrar por aquellos encargados que no tienen fecha hasta
        queryset = queryset.filter(hasta__isnull=True)
        return queryset.order_by('persona__dni')[:5] 

    def format_item_display(self, item):
        # Utiliza unidecode para eliminar las tildes
        nombre_sin_tildes = unidecode(item.persona.nombre)
        apellido_sin_tildes = unidecode(item.persona.apellido)
        return f'{nombre_sin_tildes} {apellido_sin_tildes} ({item.persona.dni})'
registry.register(EncargadoLookup)



