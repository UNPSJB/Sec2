from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.afiliados.views import AfliadosListView, index,afiliado_desafiliar, afiliado_aceptar, afiliado_ver,AfiliadoDetailView ,formEstetico
app_name="afiliados"

urlpatterns = [
    path('',index, name="index"),
    path('crear/',formEstetico, name="afiliado_crear"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="modificarAfiliado"),
    path('afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="Afiliado"),
    path('ver/<int:pk>', afiliado_ver.as_view(), name="ver_Afiliado"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),    
    #path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="baja_afiliado"),
    
]
