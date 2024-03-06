from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from apps.afiliados.models import RelacionFamiliar

from apps.personas.models import Persona
from utils.funciones import mensaje_advertencia
from .forms import SecAuthenticationForm
from apps.personas.forms import BuscadorPersonasForm
from django.contrib.auth.decorators import login_required
    

# @login_required
# def home(request):
    
#     return render(request, 'home.html', {'buscador': BuscadorPersonasForm() })
# =======
def home(request):
    """chequear si algun grupo gamiliar que sea hijo es mayor de edad"""
    relaciones_tipo_2 = RelacionFamiliar.objects.filter(tipo_relacion=2)
    
    for relacion in relaciones_tipo_2:
        
        if relacion.familiar.persona.es_mayor_edad: 
            mensaje_advertencia(request, f"Atencion! El familiar con el DNI: {relacion.familiar.persona.dni} es mayor de edad"  )

    personas = Persona.objects.all()
    return render(request, 'home.html', {'clientes': personas})

