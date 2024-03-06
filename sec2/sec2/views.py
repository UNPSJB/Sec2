from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.urls import reverse_lazy
from .forms import SecAuthenticationForm
from apps.personas.forms import BuscadorPersonasForm
from django.contrib.auth.decorators import login_required
    
# GESTION DE AFILIADOS lo quite de urls
def template_afiliado(request):
    return render(request, 'template_afiliado_home.html', {"title": "Gestion de Afiliados"})


@login_required
def home(request):
    
    return render(request, 'home.html', {'buscador': BuscadorPersonasForm() })