from django.contrib import admin
from .models import Actividad

# Register your models here.
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area')
    list_filter = ('area',)
    ordering = ('nombre', 'area')

admin.site.register(Actividad, ActividadAdmin)