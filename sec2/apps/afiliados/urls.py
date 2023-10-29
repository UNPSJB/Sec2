# Importaciones del sistema
from django.urls import path

# Importaciones locales
from .views import *
from . import views
from apps.afiliados.views import (
    index,
    afiliado_desafiliar,
    afiliado_aceptar,
    AfiliadoDetailView
)

app_name = "afiliados"

urlpatterns = [
    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="Afiliado"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="afiliado_actualizar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('mostrar/pendientes',AfliadosListPendienteView.as_view(), name="afiliado_listar_pendiente"),
    path('mostrar/activos',AfliadosListActivoView.as_view(), name="afiliado_listar_activos"),
    # FALTA IMPLEMENTAR LA PARTE DE GRUPO FAMILIAR
    path('funcionalidad-pendiente/', views.funcionalidad_pendiente, name='funcionalidad_pendiente'),
]
