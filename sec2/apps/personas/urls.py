from django.urls import path
from .views import *
# from apps.personas.views import

app_name="personas"

urlpatterns = [

# ----------------- PERSONAS -----------------

# Personalice la url y le cambie el metodo de llamada FamiliaCreateView por FamiliaCreateView1  
    # path('grupoFamiliar/<int:pk>/crear', FamiliaCreateView1, name="crear_familiar"),

]

