from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from ..personas.models import Persona

from .models import Afiliado


class AfiliadoLookup(ModelLookup):
    model = Afiliado
    search_fields = ('persona__apellido__icontains', )

registry.register(AfiliadoLookup)




class NacionalidadLookup(ModelLookup):
    model = Persona
    search_fields = ('persona__nacionalidad__icontains', )

registry.register(NacionalidadLookup)
