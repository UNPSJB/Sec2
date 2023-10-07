from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.afiliados.views import AfliadosListView, index,afiliado_desafiliar, afiliado_aceptar,AfiliadoDetailView 
app_name="afiliados"
from . import views

urlpatterns = [
    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiliado_crear"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
    path('afiliado/<int:pk>',AfiliadoDetailView.as_view(), name="Afiliado"),
    path('modificar/<int:pk>', AfiliadoUpdateView.as_view(), name="afiliado_actualizar"),
    path('mostrar/<int:pk>/aceptar', afiliado_aceptar, name="aceptar_afiliado"),
    path('mostrar/<int:pk>/desafiliar', afiliado_desafiliar, name="desafiliar_afiliado"),
]
