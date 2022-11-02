from django.contrib import admin
from django.urls import path
from .views import ActividadCreateView, ActividadDetailView, ActividadListView, ActividadUpdateView, actividad_eliminar

app_name="cursos"

urlpatterns = [
    path('actividades', ActividadListView.as_view(), name="actividades"),
    path('actividades/crear', ActividadCreateView.as_view(), name="actividad_crear"),
    path('actividades/<int:pk>', ActividadDetailView.as_view(), name="actividad_detalles"),
    path('actividades/<int:pk>/editar', ActividadUpdateView.as_view(), name="actividad_editar"),
    path('actividades/<int:pk>/eliminar', actividad_eliminar, name="actividad_eliminar"),
]
