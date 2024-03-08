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

@login_required
def home(request):    
    """Chequear si algún grupo familiar que sea hijo es mayor de edad"""

    # Filtrar roles sin fecha de finalización (hasta)
    roles_sin_fecha_hasta = Rol.objects.filter(hasta__isnull=True)
    
    # Filtrar relaciones familiares tipo 2 relacionadas con roles sin fecha de finalización
    relaciones_tipo_2 = RelacionFamiliar.objects.filter(tipo_relacion=2, familiar__in=roles_sin_fecha_hasta)

    for relacion in relaciones_tipo_2:
        if relacion.familiar.persona.es_mayor_edad: 
            mensaje_advertencia(request, f"Atención! El familiar con el DNI: {relacion.familiar.persona.dni} es mayor de edad"  )

    # Obtener personas asociadas a roles sin fecha de finalización
    personas = Persona.objects.filter(roles__in=roles_sin_fecha_hasta)
    return render(request, 'home.html', {'clientes': personas})