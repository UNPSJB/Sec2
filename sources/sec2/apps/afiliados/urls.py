from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.afiliados.views import AfliadosListView, index,afiliado_desafiliar, afiliado_aceptar, afiliado_ver

app_name="afiliados"

urlpatterns = [
    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="modificarAfiliado"),
    path('ver/<int:pk>',afiliado_ver, name="ver_Afiliado"),
    # path('ver/<int:pk>', afiliado_ver.as_view(), name="vAfiliado"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
    #path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="baja_afiliado"),
    path('algo/',include('apps.personas.urls')),
]
