# from django.shortcuts import render
from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse
from datetime import datetime  
from . import views
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from django.contrib import messages
from sec2.utils import ListFilterView
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib import messages
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Afiliado
from .forms import AfiliadoUpdateForm
from .forms import FormularioAfiliadoUpdate

# ----------------------------- AFILIADO VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
# ----------------------------- AFILIADO CREATE ----------------------------------- #
class AfiliadoCreateView(CreateView):
    model = Afiliado
    form_class = FormularioAfiliadoCreate
    success_url = reverse_lazy('afiliados:afiliado_crear')
    template_name = 'afiliados/afiliado_alta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de Afiliación"
        return context

    def form_valid(self, form):
        afiliado = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Alta de afiliado exitosa!')
        return redirect('afiliados:afiliado_listar')
    
    def form_invalid(self, form):
        fecha_nacimiento_input = self.request.POST.get('fecha_nacimiento', '')  # Obtener el valor o cadena vacía si no está presente
        # Opcionalmente, puedes agregar el valor al contexto para pasarlo a la plantilla
        context = {'form': form, 'fecha_nacimiento_input': fecha_nacimiento_input}
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return render(self.request, self.template_name, context)

# ----------------------------- AFILIADO LIST ----------------------------------- #
class AfliadosListView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar')
    template_name = 'afiliados/afiliado_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de afiliados"
        return context
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )
        return super().get_queryset()

# ----------------------------- AFILIADO LIST PENDIENTES DE ACTIVACION -------------------------- #
class AfliadosListPendienteView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar_pendiente')
    template_name = 'afiliados/afiliado_list_pendiente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Afiliados Pendientes"
        return context
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )
        return super().get_queryset()

# ----------------------------- AFILIADO LIST INACTIVO -------------------------- #
class AfliadosListActivoView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar_activos')
    template_name = 'afiliados/afiliado_list_activos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Afiliados Activos"
        return context
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_listar_activos.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )
        return super().get_queryset()

# ----------------------------- AFILIADO DETALLE ----------------------------------- #
class AfiliadoDetailView (DeleteView):
    model = Afiliado
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Datos del afiliado"
        return context
# ----------------------------- AFILIADO UPDATE ----------------------------------- #
class AfiliadoUpdateView(UpdateView):
    model = Afiliado
    form_class = FormularioAfiliadoUpdate
    template_name = 'afiliados/afiliado_detalle.html'
    success_url = reverse_lazy('afiliados:afiliado_actualizar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Afiliado"
        return context

    def form_valid(self, form):
        """Se comento la linea porque primero lo verifica y despues
        lo guarda en el form.py"""
        afiliado = form.save()
        messages.success(self.request, 'Afiliado modificado con éxito')
        return redirect('afiliados:afiliado_listar')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo errores en el formulario')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

# ----------------------------- AFILIADO ACEPTAR ----------------------------------- #

def afiliado_aceptar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    a.estado= 2
    a.save()
    # mensaje de exito
    messages.success(request, 'El afiliado ha sido aceptadov2.')
    return redirect('afiliados:afiliado_listar')

# ----------------------------- DESAFILIAR AFILIADO -----------------------------------
def afiliado_desafiliar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    fecha = datetime.now()
    a.persona.desafiliar(a,fecha)
    a.save()
    messages.success(request, 'Se ha desafiliado.')
    return redirect('afiliados:afiliado_listar')

#!ES NECESARIO ESTO??
#def desafiliar():
 #   pk=kwargs.get('pk')
  #  persona = Persona.objects.get(pk=pk)
  #  Persona.desafiliar(Persona)

#---------- HTML PARA FUNCIONALIDADES PENDIENTES
def funcionalidad_pendiente(request):
    return render(request, 'funcionalidad_pendiente.html')