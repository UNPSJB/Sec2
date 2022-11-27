from django.contrib import admin
from django.urls import path
from .views import ActividadCreateView, ActividadDetailView, ActividadListView, ActividadUpdateView, actividad_eliminar
from .views import CursoCreateView, CursoListView, index, CursoUpdateView, curso_eliminar
from .views import AulaListView, AulaCreateView, AulaDetailView, AulaUpdateView, aula_eliminar, ProfesorCreateView, ProfesorListView, ProfesorUpdateView, DictadoCreateView, DictadoListView
from .views import ClaseCreateView, ClaseListView
from .views import AlumnoCreateView

app_name="cursos"

urlpatterns = [
    path('',index, name="index"),
    
    # * ------------------------  ACTIVIDADES  ----------------------------
    path('actividades/crear', ActividadCreateView.as_view(), name="actividad_crear"),
    path('actividades', ActividadListView.as_view(), name="actividades"),
    path('actividades/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    path('actividades/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    path('actividades/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
    
    # * ------------------------  CURSOS ----------------------------------
    path('cursos', CursoListView.as_view(), name="cursos"),
    path('crear/', CursoCreateView.as_view(), name="curso_crear"),
    # path('/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    path('<int:pk>/editar', CursoUpdateView.as_view(), name="curso_editar"),
    path('<int:pk>/eliminar', curso_eliminar, name="curso_eliminar"),
    
    # * ------------------------  PROFESORES  ----------------------------
    path('profesores/crear', ProfesorCreateView.as_view(), name="profesor_crear"),
    path('profesores', ProfesorListView.as_view(), name="profesores"),
    path('profesores/<int:pk>/editar', ProfesorUpdateView.as_view(), name="profesor_modificar"),

    
    # * ------------------------  AULAS  ----------------------------------
    path('aulas', AulaListView.as_view(), name="aulas"),
    path('aulas/crear', AulaCreateView.as_view(), name="aula_crear"),
    path('aulas/<int:pk>', AulaDetailView.as_view(), name="aula_detalles"),
    path('aulas/<int:pk>/editar', AulaUpdateView.as_view(), name="aula_editar"),
    path('aulas/<int:pk>/eliminar', aula_eliminar, name="aula_eliminar"),
    
    # * ------------------------  Dictado  ----------------------------------
    path('dictado/<int:pk>', DictadoListView.as_view(), name="ver_dictados"),
    path('<int:pk>/dictado/crear', DictadoCreateView.as_view(), name="dictado_crear"),

    # * ------------------------  Clase  ------------------------------------
    path('dictado/<int:pk>/nuevaclase', ClaseCreateView.as_view(), name="clase_crear"),
    path('dictado/<int:pk>/verclases', ClaseListView.as_view(), name="ver_clases"),
    
    # * ------------------------  Alumno  ------------------------------------
    path('<int:pk>/inscripcion', AlumnoCreateView.as_view(), name="inscripcion"),
]
