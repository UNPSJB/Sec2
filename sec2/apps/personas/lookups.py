from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry
from .models import Persona  # Supongamos que tienes un modelo Persona
from .models import NACIONALIDADES  # Importa la lista de nacionalidades

class NacionalidadLookup(ModelLookup):
    model = Persona  # Usa el modelo donde se almacenarán las personas
    search_fields = ('nacionalidad__icontains',)  # Campo de búsqueda en Persona

    def get_query(self, request, term):
        # Filtrar las nacionalidades basadas en la lista NACIONALIDADES
        nacionalidades = [n for n in NACIONALIDADES if term.lower() in n[1].lower()]
        return nacionalidades

registry.register(NacionalidadLookup)





class PersonaLookup(ModelLookup):
    model = Persona
    search_fields = ('apellido__icontains', )

registry.register(PersonaLookup)
