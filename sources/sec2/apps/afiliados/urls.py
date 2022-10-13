from django.contrib import admin
from django.urls import path
from .views import FormularioAfiliadoView
urlpatterns = [
    path('alta-afiliado/',FormularioAfiliadoView.index, name='altaAfiliado'),
    path('guardar-afiliado/',FormularioAfiliadoView.procesarFormulario, name='guardarAfiliado'),
]
