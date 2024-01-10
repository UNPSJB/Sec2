from django.shortcuts import render
from apps.alquileres.forms import *
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime  
from .models import Alquiler, Salon
from .forms import *
from sec2.utils import ListFilterView
from django.db import transaction  # Agrega esta línea para importar el módulo transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
#CONSTANTE
from utils.constants import *

# Create your views here.
# ----------------------------- ALQUILER VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# ----------------------------- CREATE DE SALON  ----------------------------------- #

class SalonCreateView(CreateView):
    model = Salon
    form_class = SalonrForm
    template_name = 'salon_form.html'
    success_url = reverse_lazy('alquiler:salon_listar')
    title = "Formulario Alta de Salon"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de salon exitosa!')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)
    
# ----------------------------- DETAIL DE SALON  ----------------------------------- #
class SalonDetailView(DetailView):
    model = Salon
    template_name = 'Alquiler/salon_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Salon: {self.object.nombre}"
        #context['tituloListado'] = 'Dictados Asociados'
        return context
    
# ----------------------------- LIST DE SALON  ----------------------------------- #


# ----------------------------- UPDATE DE SALON  ----------------------------------- #

class SalonUpdateView(UpdateView):
    model = Salon
   # form_class = AlquilerForm
    template_name = 'alquiler/salon_form.html'
    success_url = reverse_lazy('alquiler:salon')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar salon"
        return context
    
    def form_valid(self, form):
        curso = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> salon modificado con éxito')
        return redirect('alquiler:salon_detalle', pk=curso.pk)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form) 