from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from apps.afiliados.models import RelacionFamiliar

from apps.personas.models import Persona
from utils.funciones import mensaje_advertencia
from .forms import SecAuthenticationForm
from apps.personas.forms import BuscadorPersonasForm

# @login_required(login_url='/login')
def login(request):
    no_user = False
    form = SecAuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return redirect(reverse_lazy('home'))
        else:
            # TODO: revisar. Añado el flag porque en este caso user es None en el server 
            # pero AnonymousUser en el template y no puedo mostrar los msjs de error en el template.
            no_user = True 
    return render(request, 'login.html', {  
        "title": "SEC2 | Iniciar sesión", 
        "form": SecAuthenticationForm(), 
        "no_user": no_user
    })
    
    
def home(request):
    """chequear si algun grupo gamiliar que sea hijo es mayor de edad"""
    relaciones_tipo_2 = RelacionFamiliar.objects.filter(tipo_relacion=2)
    
    for relacion in relaciones_tipo_2:
        
        if relacion.familiar.persona.es_mayor_edad: 
            mensaje_advertencia(request, f"Atencion! El familiar con el DNI: {relacion.familiar.persona.dni} es mayor de edad"  )

    personas = Persona.objects.all()
    return render(request, 'home.html', {'clientes': personas})
