from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.personas.views import FamiliaCreateView1

app_name="personas"

urlpatterns = [

# ----------------- PERSONAS -----------------

# Personalice la url y le cambie el metodo de llamada FamiliaCreateView por FamiliaCreateView1  
    path('afiliado/<int:pk>/grupoFamiliar/crear', FamiliaCreateView1, name="crear_familiar"),
    # path('grupoFamiliar/<int:pk>/crear', FamiliaCreateView1, name="crear_familiar"),

]

