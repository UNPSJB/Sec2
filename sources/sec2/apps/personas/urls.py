from django.contrib import admin
from django.urls import path, include
from .views import *
from apps.personas.views import FamiliaCreateView

app_name="personas"

urlpatterns = [
    
    # ----------------- PERSONAS -----------------
     path('grupoFamiliar/<int:pk>/crear', FamiliaCreateView, name="crear_familiar"),
]

