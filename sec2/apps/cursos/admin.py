from django.contrib import admin
from .models import Actividad, Curso, Dictado, Aula, Alumno, Profesor, Asistencia_alumno, Asistencia_profesor

# Register your models here.
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area')
    list_filter = ('area',)
    ordering = ('nombre', 'area')

admin.site.register(Actividad, ActividadAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'nombre','descripcion')
    #list_filter = ('actividad')
    #ordering = ('actividad')

admin.site.register(Curso, CursoAdmin)

class DictadoAdmin(admin.ModelAdmin):
    # Asegúrate de que los campos mencionados en list_display sean atributos o métodos válidos
    list_display = ('nombre', 'costo')

    # Otros atributos o métodos de configuración del ModelAdmin

# Registrar el modelo con el nuevo ModelAdmin
admin.site.register(Dictado, DictadoAdmin)

class AulaAdmin (admin.ModelAdmin):
    list_display= ('denominacion','tipo','cupo')



admin.site.register(Aula, AulaAdmin)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Asistencia_alumno)
admin.site.register(Asistencia_profesor)