from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.afiliados.views import AfliadosListView, index,afiliado_desafiliar, afiliado_aceptar, afiliado_ver,AfiliadoDetailView 
app_name="afiliados"
from . import views

urlpatterns = [

# IMPORTANTE
# para crear afiliado la url seria: afiliados/afiliado/crear

    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="Afiliado"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="modificarAfiliado"),

    #cambiar esto
    path('afiliado_modificado_exitosamente/', views.afiliado_modificado_exitosamente, name='afiliado_modificado_exitosamente'),

    # path('afiliado/<int:pk>',views.detalleAfiliado, name="Afiliado"),
    path('ver/<int:pk>', afiliado_ver.as_view(), name="ver_Afiliado"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
    #path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="baja_afiliado"),
]
