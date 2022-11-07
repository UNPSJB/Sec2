from django.contrib import admin

from apps import afiliados
from .models import Persona
from .models import Rol

# Register your models here.
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'fecha_nacimiento')
    list_filter = ('nombre','apellido')
    ordering = ('nombre', 'fecha_nacimiento')

admin.site.register(Persona, PersonaAdmin)


