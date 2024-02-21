# Importaciones del sistema
from django.urls import path

# Importaciones locales
from .views import *
from . import views
from apps.afiliados.views import *


app_name = "afiliados"

urlpatterns = [
    path('',index, name="index"),
    path('afiliados/afiliado/crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    
    path('afiliados/listar',AfliadosListView.as_view(), name="afiliado_listar"),
    path('afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="afiliado_detalle"),


    # AFILIACION - DESAFILIACIÓN
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="afiliado_actualizar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
    
    #GRUPO FAMILIAR
    path('afiliado/<int:pk>/grupoFamiliar/crear', FamiliaCreateView.as_view(), name="crear_familiar"),
    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>', FamiliarDetailView.as_view(), name="familiar_detalle"),
    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>/editar', FamiliarUpdateView.as_view(), name="familiar_editar"),
    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>/eliminar', familiar_eliminar, name="familiar_eliminar"),
    
    #ACCEDIDOS DESDE LA APLICACION DE CURSOS
    path('afiliado/grupoFamiliar/familia/<int:familiar_pk>', FamiliarDetailView_.as_view(), name="familiar_detalle_"),
    path('afiliado/grupoFamiliar/familia/<int:familiar_pk>/editar', FamiliarUpdateView_.as_view(), name="familiar_editar_"),

    # path('mostrar/pendientes',AfliadosListPendienteView.as_view(), name="afiliado_listar_pendiente"),
    # path('mostrar/activos',AfliadosListActivoView.as_view(), name="afiliado_listar_activos"),
    # FALTA IMPLEMENTAR LA PARTE DE GRUPO FAMILIAR
    # path('funcionalidad-pendiente/', views.funcionalidad_pendiente, name='funcionalidad_pendiente'),
]