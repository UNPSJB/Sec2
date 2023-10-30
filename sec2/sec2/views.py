from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
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
    
    
# GESTION DE AFILIADOS lo quite de urls
def template_afiliado(request):
    return render(request, 'template_afiliado_home.html', {"title": "Gestion de Afiliados"})

def home(request):
    return render(request, 'home.html', {'buscador': BuscadorPersonasForm() })