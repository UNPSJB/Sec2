from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from unidecode import unidecode

from apps.afiliados.models import Afiliado, Familiar
from apps.personas.models import Rol

from selectable.base import LookupBase

class DniAfiliadoLookup(LookupBase):
    def get_query(self, request, term):
        queryset = self.get_queryset(term)  # Pasa el término de búsqueda a get_queryset
        # if term:
        return queryset

    def get_queryset(self, term):
        afiliados = Afiliado.objects.filter(persona__dni__icontains=term)[:3]  # Filtra por DNI y toma los primeros 3 resultados
        queryset = [
            {"id": afiliado.persona.dni}
            for afiliado in afiliados
        ]
        return queryset
    
    def get_item_value(self, item):
        return item.get("id", "")

    
    def get_item_id(self, item):
        return item.get("id", "")

    
    def get_item_label(self, item):
        return item.get("id", "")
    
    def get_item_value(self, item):
        if isinstance(item, dict):  # Verifica si item es un diccionario
            return item.get("id", "")  # Utiliza .get() para obtener el valor de "id"
        else:
            return ""  # Si item no es un diccionario, devuelve un valor predeterminado o maneja el caso según sea necesario

registry.register(DniAfiliadoLookup)

class DniFamiliarLookup(LookupBase):
    def get_query(self, request, term):
        queryset = self.get_queryset(term)  # Pasa el término de búsqueda a get_queryset
        # if term:
        return queryset

    def get_queryset(self, term):
        familiares = Familiar.objects.filter(persona__dni__icontains=term)[:3]  # Filtra por DNI y toma los primeros 3 resultados
        queryset = [
            {"id": familiar.persona.dni}
            for familiar in familiares
        ]
        return queryset
    
    def get_item_value(self, item):
        return item.get("id", "")

    
    def get_item_id(self, item):
        return item.get("id", "")

    
    def get_item_label(self, item):
        return item.get("id", "")
    
    def get_item_value(self, item):
        if isinstance(item, dict):  # Verifica si item es un diccionario
            return item.get("id", "")  # Utiliza .get() para obtener el valor de "id"
        else:
            return ""  # Si item no es un diccionario, devuelve un valor predeterminado o maneja el caso según sea necesario

registry.register(DniFamiliarLookup)


class AfiLookup(ModelLookup):
    model = Afiliado
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
registry.register(AfiLookup)

class CuitEmpleadorLookup(LookupBase):
    def get_query(self, request, term):
        queryset = self.get_queryset(term)
        # if term:
            # Puedes agregar lógica de filtrado si lo deseas
            # pass
        return queryset

    def get_queryset(self, term):
        afiliados = Afiliado.objects.all().distinct("cuit_empleador")
        queryset = [
            {"id": afiliado.cuit_empleador,
             "nombre": afiliado.razon_social}
            for afiliado in afiliados
        ]
        return queryset
    
    def get_item_value(self, item):
        if isinstance(item, dict):
            return item.get("id", "")
        else:
            return ""  # Si item no es un diccionario, devuelve un valor predeterminado o maneja el caso según sea necesario
    
    def get_item_id(self, item):
        return item.get("id", "")
    
    def get_item_label(self, item):
        return item.get("id", "")
    
    def format_item_display(self, item):
        if isinstance(item, dict):  # Verifica si item es un diccionario
            return item.get("id", "")  # Utiliza .get() para obtener el valor de "id"
        else:
            return ""  # Si item no es un diccionario, devuelve un valor predeterminado o maneja el caso según sea necesario

registry.register(CuitEmpleadorLookup)  


class EmpleadorLookup(LookupBase):
    def get_query(self, request, term):
        queryset = self.get_queryset()
        # if term:
            # Puedes agregar lógica de filtrado si lo deseas
            # pass
        return queryset

    def get_queryset(self):
        afiliados = Afiliado.objects.all().distinct("cuit_empleador", "razon_social")
        queryset = [
            {"id": afiliado.cuit_empleador,
             "nombre": afiliado.razon_social}
            for afiliado in afiliados
        ]
        return queryset
    
    def get_item_value(self, item):
        return item["id"] + ' ' + item["nombre"]
    
    def get_item_id(self, item):
        return item["id"]
    
    def get_item_label(self, item):
        return item["id"] + ' ' + item["nombre"]
    
    def format_item_display(self, item):
        return f'{item["id"]} - {item["nombre"]}'  # Esto es opcional, se muestra en la lista desplegable

registry.register(EmpleadorLookup)  