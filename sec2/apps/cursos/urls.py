from django.urls import path
# from views import index, actividad_eliminar, curso_eliminar, registrarAsistenciaProfesor, registrarAlumnoADictado, registrarAsistenciaAlumno, aula_eliminar
from .views.actividad_views import *
from .views.curso_views import *
from .views.dictado_views import *
from .views.horario_views import *
from .views.clase_views import *
from .views.profesor_views import *
from .views.alumno_views import *
from .views.aula_views import *
from .views.pago_views import *
from .views.views import *

app_name="cursos"

urlpatterns = [
    # PRINCIPAL
    path('',index, name="index"),

    # AULAS
    path('aulas/crear', AulaCreateView.as_view(), name="aula_crear"),
    path('aulas/<int:pk>', AulaDetailView.as_view(), name="aula_detalle"),
    path('aulas/<int:pk>/editar', AulaUpdateView.as_view(), name="aula_editar"),
    path('aulas/<int:pk>/eliminar', aula_eliminar, name="aula_eliminar"),
    path('aulas/', AulaListView.as_view(), name="aula_listado"), #list
    
    # CURSOS
    path('cursos/curso/crear/', CursoCreateView.as_view(), name="curso_crear"),
    path('cursos/curso/<int:pk>', CursoDetailView.as_view(), name="curso_detalle"),
    path('cursos/curso/<int:pk>/editar', CursoUpdateView.as_view(), name="curso_editar"),
    path('cursos/curso/<int:pk>/eliminar', curso_eliminar, name="curso_eliminar"),
    path('cursos/listado', CursoListView.as_view(), name="curso_listado"),

    # DICTADOS (accedido desde cursos)
    path('cursos/curso/<int:pk>/dictados/dictado/crear', DictadoCreateView.as_view(), name="dictado_crear"),
    path('cursos/curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>', DictadoDetailView.as_view(), name="dictado_detalle"),
    path('cursos/curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>/editar', DictadoUpdateView.as_view(), name="dictado_editar"),

    # HORARIO (accedido desde dictado)
    path('curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>/horarios/horario/crear/', HorarioCreateView.as_view(), name='horario_crear'),

    # CLASE (accedido desde dictaod)
    path('cursos/curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>/clases/clase/crear', ClaseCreateView.as_view(), name="clase_crear"),



#------------------------ INCHEQUEADO ------------------------
    # # ACTIVIDADES
    # path('actividades/actividad/crear', ActividadCreateView.as_view(), name="actividad_crear"),
    # path('actividades/actividad/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalle"),
    # path('actividades/actividad/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    # path('actividades/actividad/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
    # path('actividades/listado', ActividadListView.as_view(), name="actividad_listado"),

    path('cursos/curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>/clases/clase/<int:clase_pk>', ClaseDetailView.as_view(), name="clase_detalle"),

    
    # path('cursos/curso/<int:curso_pk>/dictados/dictado/<int:dictado_pk>/clases/clase/<int:clase_pk>/horarios/horario/<int:horario_pk>', HorarioCreateView.as_view(), name="clase_detalle"),

	# NO UTILIZADO POR EL MOMENTO
	path('cursos/<int:pk>/dictados', DictadoListView.as_view(), name="dictado_listado"),
    path('dictado/<int:pk>/verclases', ClaseListView.as_view(), name="ver_clases"),#se accede desde el dictado

    # TODO: ------------------------  PROFESORES  ----------------------------
    path('profesores/crear', ProfesorCreateView.as_view(), name="profesor_crear"),
    path('profesores', ProfesorListView.as_view(), name="profesores"),
    path('profesores/<int:pk>/editar', ProfesorUpdateView.as_view(), name="profesor_modificar"),
    # path('profesores/<int:pk>/eliminar', actividad_eliminar, name="profesor_eliminar"),
    
    


    # path('<int:pk>/dictado/alumnos',  AlumnosDelDictadoListView.as_view(), name="alumnos_dictado"),#se accede desde el curso
    path('<int:pk>/dictado/<int:dpk>/alumnos',  agregarAlumnoCursoListView.as_view(), name="alumnos_dictado_curso"),#se accede desde dictado
    path('<int:pk>/dictado/inscribir/<int:apk>',  registrarAlumnoADictado, name="carga_alumno_dictado"),
    
    
    # * ------------------------  Alumno  ------------------------------------
    path('<int:pk>/inscripcion', AlumnoCreateView.as_view(), name="inscripcion"),#se accede desde el curso
   
    
    # * ------------------------  Asistencia  ------------------------------------
    path('<int:pk>/dictado/profesor',  ProfesorDelDictadoListView.as_view(), name="profesor_dictado"),
    path('<int:pk>/dictado/profesor/<int:ppk>/presente',  registrarAsistenciaProfesor, name="asistencia_profesor"),
    path('<int:pk>/dictado/alumnos/<int:apk>/asistencia', registrarAsistenciaAlumno, name="asistencia_alumno"),
    
    # path('<int:pk>/inscriptos', AlumnosListView.as_view(), name="ver_inscriptos"),
#    path('<int:dpk>/dictado/<int:pk>/asistencia', registrarAsistenciaAlumno, name="asistencia_alumno"),
   # path('<int:pk>/inscriptos', AlumnosListView.as_view(), name="ver_inscriptos"),
    # path('<int:pk>/inscriptos', alumno_inscribir, name="completar_inscripcion"),
    path('pagoalumno', PagoAlumnoCreateView.as_view(), name="pago_alumno"),
    
]
