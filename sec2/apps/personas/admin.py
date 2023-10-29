from django.contrib import admin

from apps import afiliados
from .models import Persona
from .models import Rol

# Register your models here.
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellido', 'nombre', 'fecha_nacimiento')
    list_filter = ('dni','apellido')
    ordering = ('dni', 'apellido')

admin.site.register(Persona, PersonaAdmin)


