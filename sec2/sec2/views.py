from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from apps.afiliados.models import Afiliado, RelacionFamiliar

from apps.alquileres.models import Alquiler
from apps.personas.models import Persona, Rol
from apps.afiliados.forms import AfiliadoFormSearch
from utils.funciones import mensaje_advertencia
from .forms import SecAuthenticationForm
from apps.personas.forms import PersonaFormSearch
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.contrib.auth.models import User
    


def obtener_permisos_user_string(user):
    permisos = user.user_permissions.all()
    nombres_permisos = [permiso.codename for permiso in permisos]
    print(nombres_permisos)
    return nombres_permisos
        # Imprimir los nombres de los permisos



def cambiar_estado_alquileres():
    alquileres = Alquiler.objects.filter(estado=1, fecha_alquiler__lt=datetime.now())
    alquileres_hoy = Alquiler.objects.filter(estado=1, fecha_alquiler__date=date.today())

    for alquiler in alquileres:
        alquiler.estado = 3  # Cambiar estado a "Finalizado"
        alquiler.save()

    for alquiler_hoy in alquileres_hoy:
        alquiler_hoy.estado = 2  # Cambiar estado a "En curso"
        alquiler_hoy.save()
    
    
@login_required(login_url='/login/')
@login_required
def home(request):
    cambiar_estado_alquileres()
    """Chequear si algún grupo familiar que sea hijo es mayor de edad"""
    permisos = obtener_permisos_user_string(request.user)
    # Filtrar roles sin fecha de finalización (hasta)
    roles_sin_fecha_hasta = Rol.objects.filter(hasta__isnull=True)

    form = PersonaFormSearch()

    
    # Filtrar relaciones familiares tipo 2 relacionadas con roles sin fecha de finalización
    relaciones_tipo_2 = RelacionFamiliar.objects.filter(tipo_relacion=2, familiar__in=roles_sin_fecha_hasta)

    for relacion in relaciones_tipo_2:
        if relacion.familiar.persona.es_mayor_edad: 
           mensaje_advertencia(request, f"Atencion! El familiar con el DNI: {relacion.familiar.persona.dni} es mayor de edad"  )

    personas = personas = Persona.objects.filter(roles__in=roles_sin_fecha_hasta)
    return render(request, 'home.html', {'clientes': personas, "permisos":permisos, "form":form})

     