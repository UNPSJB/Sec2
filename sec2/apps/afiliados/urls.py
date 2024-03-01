# Importaciones del sistema
from django.urls import path

# Importaciones locales
from .views import *
from . import views
from apps.afiliados.views import *


app_name = "afiliados"

urlpatterns = [
    path('',index, name="index"),

    #AFILIADO
    path('afiliados/afiliado/crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('afiliados/afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="afiliado_detalle"),
    path('afiliados/afiliado/<int:pk>/editar', AfiliadoUpdateView.as_view(), name="afiliado_actualizar"),
    path('afiliados/listar',AfliadosListView.as_view(), name="afiliado_listar"),
    path('afiliados/afiliado/<int:pk>/<str:accion>/<str:origen>/', afiliado_afiliar_desafiliar, name="afiliado_afiliar_desafiliar"),
    #ALTA GRUPO FAMILIAR (accedido desde afiliado)
    path('afiliado/<int:pk>/grupoFamiliar/crear', FamiliaCreateView.as_view(), name="crear_familiar"),

    #GRUPO FAMILIAR
    path('grupofamiliar/crear', alta_familiar, name="crear_familiar_directo"),

    #RELACION AFILIADO-GRUPO FAMILIAR
    path('grupofamiliar/listado', RelacionFamiliarListView.as_view(), name="grupo_familiar_listar"),
    path('afiliados/afiliado/<int:pk>/generarnota', confeccionarNota ,name="confeccionar_nota"),


    ## tiene que tener laopcion de llevarlo a mi misma vista, a otra ventana
    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>/<str:ventana>/', FamiliarDetailView.as_view(), name="familiar_detalle"),


    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>/editar', FamiliarUpdateView.as_view(), name="familiar_editar"),
    path('afiliado/<int:pk>/grupoFamiliar/familia/<int:familiar_pk>/eliminar', familiar_eliminar, name="familiar_eliminar"),
    

    #ACCEDIDOS DESDE LA APLICACION DE CURSOS
    path('afiliado/grupoFamiliar/familia/<int:familiar_pk>', FamiliarDetailView_.as_view(), name="familiar_detalle_"),
    path('afiliado/grupoFamiliar/familia/<int:familiar_pk>/editar', FamiliarUpdateView_.as_view(), name="familiar_editar_"),
]