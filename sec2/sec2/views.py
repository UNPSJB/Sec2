from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from apps.afiliados.models import RelacionFamiliar

from apps.personas.models import Persona, Rol
from utils.funciones import mensaje_advertencia
from .forms import SecAuthenticationForm
from apps.personas.forms import BuscadorPersonasForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
    

# @login_required
# def home(request):
    
#     return render(request, 'home.html', {'buscador': BuscadorPersonasForm() })
# =======




def obtener_permisos_user_string(user):
    permisos = user.user_permissions.all()
    nombres_permisos = [permiso.codename for permiso in permisos]
    print(nombres_permisos)
    return nombres_permisos
        # Imprimir los nombres de los permisos



@login_required(login_url='/login/')
def home(request):    
    """Chequear si algún grupo familiar que sea hijo es mayor de edad"""
    permisos = obtener_permisos_user_string(request.user)
    # Filtrar roles sin fecha de finalización (hasta)
    roles_sin_fecha_hasta = Rol.objects.filter(hasta__isnull=True)

    
    # Filtrar relaciones familiares tipo 2 relacionadas con roles sin fecha de finalización
    relaciones_tipo_2 = RelacionFamiliar.objects.filter(tipo_relacion=2, familiar__in=roles_sin_fecha_hasta)

    for relacion in relaciones_tipo_2:
        if relacion.familiar.persona.es_mayor_edad: 
           mensaje_advertencia(request, f"Atencion! El familiar con el DNI: {relacion.familiar.persona.dni} es mayor de edad"  )

    personas = personas = Persona.objects.filter(roles__in=roles_sin_fecha_hasta)
    return render(request, 'home.html', {'clientes': personas, "permisos":permisos})

     