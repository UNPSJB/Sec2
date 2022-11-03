from django.contrib import admin
from django.urls import path
from .views import ActividadCreateView, ActividadDetailView, ActividadListView, ActividadUpdateView, actividad_eliminar
from .views import CursoCreateView

app_name="cursos"

urlpatterns = [
    
    # * ------------------------  CURSOS ----------------------------------
    # path('cursos', ActividadListView.as_view(), name="cursos"), ## ! no anda
    path('crear/', CursoCreateView.as_view(), name="curso_crear"),
    # path('actividades/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    # path('actividades/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    # path('actividades/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
    
    # * ------------------------  ACTIVIDADES  ----------------------------
    path('actividades', ActividadListView.as_view(), name="actividades"), ## ! no anda 
    path('actividades/crear', ActividadCreateView.as_view(), name="actividad_crear"),
    path('actividades/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    path('actividades/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    path('actividades/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
]
