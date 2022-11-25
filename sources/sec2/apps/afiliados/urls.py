from django.contrib import admin
from django.urls import path
from .views import *
from apps.afiliados.views import AfliadosListView, index,afiliado_desafiliar, afiliado_aceptar

app_name="afiliados"

urlpatterns = [

    #path('',AfiliadoCreateView.as_view(), name="index"),
   # path('crear/',AfiliadoCreateView.as_view(), name="crearAfiliado"),
   # path('mostrar/',AfliadosListView.as_view(), name="mostrarAfiliados"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="modificarAfiliado"),
    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
    #path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="baja_afiliado"),
]
