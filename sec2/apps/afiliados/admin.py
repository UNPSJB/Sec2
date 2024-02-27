from django.contrib import admin
from .models import Afiliado, Familiar, RelacionFamiliar
from apps.personas.models import Rol

class AfiliadoAdmin(admin.ModelAdmin):
    list_display = ('estado', 'razon_social', 'categoria_laboral')
admin.site.register(Afiliado, AfiliadoAdmin)

class FamiliarAdmin(admin.ModelAdmin):
    list_display = ('tipo_relacion', 'activo')
admin.site.register(Familiar, FamiliarAdmin)

class RelacionFamiliarAdmin(admin.ModelAdmin):
    list_display = ('afiliado', 'familiar')
admin.site.register(RelacionFamiliar, RelacionFamiliarAdmin)

admin.site.register(Rol)