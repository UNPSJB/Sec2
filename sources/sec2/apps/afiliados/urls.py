from django.contrib import admin
from django.urls import path
from .views import *
from apps.afiliados.views import AfliadosListView, index

app_name="afiliados"

urlpatterns = [

    path('',index, name="index"),
    path('crear/',AfiliadoCreateView.as_view(), name="afiiado_crear"),
    path('mostrar/',AfliadosListView.as_view(), name="afiliado_listar"),
]
