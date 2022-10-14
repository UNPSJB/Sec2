from django.contrib import admin
from django.urls import path
from .views import *

app_name="afiliados"

urlpatterns = [
    
    # ----------------- AFILIADOS -----------------

    path('',AfiliadoCreateView.as_view(), name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="crearAfiliado"),
    
    # path('alta-afiliado/',FormularioAfiliadoView.index, name='altaAfiliado'),
    # path('guardar-afiliado/',FormularioAfiliadoView.procesarFormulario, name='guardarAfiliado'),
]
