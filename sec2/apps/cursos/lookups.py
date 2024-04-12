from __future__ import unicode_literals

from selectable.base import ModelLookup
from apps.cursos.models import Actividad

from selectable.registry import registry

class ActividadLookup(ModelLookup):
    model = Actividad
    search_fields = ('nombre__icontains', )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

registry.register(ActividadLookup)


class PagoAlumnoLookup(ModelLookup):
    model = Actividad
    search_fields = ('nombre__icontains', )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

registry.register(PagoAlumnoLookup)

