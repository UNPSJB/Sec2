from django.contrib import admin
from .models import Alumno, Clase, Curso, Aula, Dictado, Horario, Reserva

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

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('display_nombre_completo', 'display_dictados')

    def display_nombre_completo(self, obj):
        return f"{obj.persona.nombre} {obj.persona.apellido}"

    def display_dictados(self, obj):
        return ", ".join([str(dictado) for dictado in obj.dictados.all()])

    display_nombre_completo.short_description = 'Nombre Completo'
    display_dictados.short_description = 'Dictados'

admin.site.register(Alumno, AlumnoAdmin)


# admin.site.register(Alumno)
# admin.site.register(Profesor)
# admin.site.register(Asistencia_alumno)
# admin.site.register(Asistencia_profesor)
