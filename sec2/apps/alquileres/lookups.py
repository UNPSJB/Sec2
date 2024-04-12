from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from unidecode import unidecode

from apps.alquileres.models import Salon
from apps.personas.models import Rol


class SalonLookup(ModelLookup):
    model = Salon
    search_fields = ('nombre__icontains', )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(fechaBaja__isnull=True).order_by('nombre')
        return queryset
registry.register(SalonLookup)
