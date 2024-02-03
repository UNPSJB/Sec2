from django.contrib import admin
from .models import Actividad, Alumno, Clase, Curso, Aula, Dictado, Horario, Reserva

class AulaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'capacidad')
admin.site.register(Aula, AulaAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
admin.site.register(Curso, CursoAdmin)

class DictadoAdmin(admin.ModelAdmin):
    list_display = ('fecha','cupo')
admin.site.register(Dictado, DictadoAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('fecha','aula', 'horario')
admin.site.register(Reserva, ReservaAdmin)

class HorarioAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio',)
admin.site.register(Horario, HorarioAdmin)

class ClaseAdmin(admin.ModelAdmin):
    list_display = ('reserva',)
admin.site.register(Clase, ClaseAdmin)

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
admin.site.register(Actividad, ActividadAdmin)

admin.site.register(Alumno)

# admin.site.register(Profesor)
# admin.site.register(Asistencia_alumno)
# admin.site.register(Asistencia_profesor)
