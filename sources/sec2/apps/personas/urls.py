from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [

    # ----------------- PERSONAS -----------------

    
     path('home/<int:pk>/familia', FamiliaCreateView, name='familiaPersona'),
]

