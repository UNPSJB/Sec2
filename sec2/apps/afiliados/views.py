from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime  
from .models import Afiliado
from .forms import *
from sec2.utils import ListFilterView

#CONSTANTE
from utils.constants import *

# ----------------------------- AFILIADO VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# ----------------------------- AFILIADO CREATE ----------------------------------- #
class AfiliadoCreateView(CreateView):
    model = Persona
    form_class = AfiliadoPersonaForm #utiliza un formulario unificado
    template_name = 'afiliados/afiliado_alta.html'
    success_url = reverse_lazy('afiliados:afiliado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de Afiliación"
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        existing_person = Persona.objects.filter(dni=dni).first()

        if existing_person:
            messages.error(self.request, f'{ICON_ERROR} La persona ya está registrada en el sistema.')
            form = AfiliadoPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
            )
            persona.save()

            # Crear una instancia de Afiliado
            afiliado = Afiliado(
                persona=persona,
                razon_social=form.cleaned_data["razon_social"],
                categoria_laboral=form.cleaned_data["categoria_laboral"],
                rama=form.cleaned_data["rama"],
                sueldo=form.cleaned_data["sueldo"],
                fechaAfiliacion=form.cleaned_data["fechaAfiliacion"],
                fechaIngresoTrabajo=form.cleaned_data["fechaIngresoTrabajo"],
                cuit_empleador=form.cleaned_data["cuit_empleador"],
                localidad_empresa=form.cleaned_data["localidad_empresa"],
                domicilio_empresa=form.cleaned_data["domicilio_empresa"],
                horaJornada=form.cleaned_data["horaJornada"],
            )
            print("VOY A ENTRAR EN EL SAVE")
            afiliado.save()

            messages.success(self.request, f'{ICON_CHECK} Alta de afiliado exitosa!')
            return redirect('afiliados:afiliado_listar')


    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION}')
        return super().form_invalid(form)

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
        messages.success(self.request, 'f{ICON_CHECK} Afiliado modificado con éxito')
        return redirect('afiliados:afiliado_listar')

    def form_invalid(self, form):
        messages.error(self.request, f'{ICON_ERROR} Hubo errores en el formulario')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

# ----------------------------- AFILIADO ACEPTAR ----------------------------------- #

def afiliado_aceptar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    a.estado= 2
    a.save()
    # mensaje de exito
    messages.success(request, f'{ICON_CHECK} El afiliado ha sido aceptado.')
    return redirect('afiliados:afiliado_listar')

# ----------------------------- DESAFILIAR AFILIADO -----------------------------------
def afiliado_desafiliar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    fecha = datetime.now()
    a.persona.desafiliar(a,fecha)
    a.save()
    messages.success(request, 'f{ICON_CHECK} Se ha desafiliado.')
    return redirect('afiliados:afiliado_listar')

#!ES NECESARIO ESTO??
#def desafiliar():
 #   pk=kwargs.get('pk')
  #  persona = Persona.objects.get(pk=pk)
  #  Persona.desafiliar(Persona)

#---------- HTML PARA FUNCIONALIDADES PENDIENTES
def funcionalidad_pendiente(request):
    return render(request, 'funcionalidad_pendiente.html')