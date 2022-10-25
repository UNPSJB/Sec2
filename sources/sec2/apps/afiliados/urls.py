from django.contrib import admin
from django.urls import path
from .views import *
from apps.afiliados.views import AfliadosListView

app_name="afiliados"

urlpatterns = [
    
    # ----------------- AFILIADOS -----------------

    path('',AfiliadoCreateView.as_view(), name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="crearAfiliado"),
    path('mostrar/',AfliadosListView.as_view(), name="mostrarAfiliados"),
    # path('alta-afiliado/',FormularioAfiliadoView.index, name='altaAfiliado'),
    # path('guardar-afiliado/',FormularioAfiliadoView.procesarFormulario, name='guardarAfiliado'),
]
