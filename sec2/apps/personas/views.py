from django.shortcuts import get_object_or_404, render

from apps.afiliados.models import Afiliado
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

"""
CLASE CREADA DE PRUEBA PORQUE NO FUNCABA EL ALTA DE GRUPO FAMILIAR
class FamiliaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    success_url = reverse_lazy('personas:crear_familiar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de Grupo Familiar"
        return context """


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm #utiliza un formulario unificado
    template_name = 'personas/persona_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de Afiliación"
        return context


