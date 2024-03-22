from django.shortcuts import render
from .views import CustomLoginView, CreacionUsuarios,cerrar_session
from django.urls import path

app_name = "users"

urlpatterns = [
  path('login/', CustomLoginView.as_view(), name='login'),
  path('registrar_usuarios/', CreacionUsuarios.as_view(), name='user_register'),
  path('cerrar_session/',cerrar_session,name='cerrar_session'),

   ]