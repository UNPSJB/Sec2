from apps.personas.models import Rol
from selectable.base import ModelLookup
from selectable.registry import registry


class RolLookup(ModelLookup):
    model = Rol
    search_fields = ('persona__dni__icontains', 'persona__nombre__icontains','persona__nombre__icontains')
    
    def get_query(self, request, term):
        queryset = super().get_query(request, term)
        # Ordenar por alias y luego por posición, y limitar a los primeros 5 resultados
        return queryset.order_by('persona__dni')[:5] 

registry.register(RolLookup)