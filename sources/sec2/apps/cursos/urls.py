from django.contrib import admin
from django.urls import path
from .views import ActividadCreateView, ActividadDetailView, ActividadListView, ActividadUpdateView, actividad_eliminar
from .views import CursoCreateView, CursoListView, index
from .views import AulaListView, AulaCreateView, AulaDetailView, AulaUpdateView, aula_eliminar

app_name="cursos"

urlpatterns = [
    path('',index, name="index"),
    # * ------------------------  CURSOS ----------------------------------
    path('cursos', CursoListView.as_view(), name="cursos"),
    path('crear/', CursoCreateView.as_view(), name="curso_crear"),
    # path('/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    # path('/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    # path('/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
    
    # * ------------------------  ACTIVIDADES  ----------------------------
    path('actividades', ActividadListView.as_view(), name="actividades"),
    path('actividades/crear', ActividadCreateView.as_view(), name="actividad_crear"),
    path('actividades/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    path('actividades/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    path('actividades/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
    
    # * ------------------------  AULAS  ----------------------------------
    path('aulas', AulaListView.as_view(), name="aulas"),
    path('aulas/crear', AulaCreateView.as_view(), name="aula_crear"),
    path('aulas/<int:pk>', AulaDetailView.as_view(), name="aula_detalles"),
    path('aulas/<int:pk>/editar', AulaUpdateView.as_view(), name="aula_editar"),
    path('aulas/<int:pk>/eliminar', aula_eliminar, name="aula_eliminar"),
]
