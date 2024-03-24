from django.shortcuts import get_object_or_404, render
from apps.afiliados.views import existe_persona_activa
from apps.alquileres.forms import *
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import DetailView, ListView
from apps.personas.models import Rol

from utils.funciones import mensaje_advertencia, mensaje_error, mensaje_exito  
from .models import Alquiler, Salon, Servicio, Encargado, Afiliado, Pago_alquiler
from .forms import *
from sec2.utils import ListFilterView
from django.db import transaction  # Agrega esta línea para importar el módulo transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
#CONSTANTE
from utils.constants import *

# Create your views here.
# ----------------------------- ALQUILER VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# ----------------------------- CREATE DE ENCARGADO  ----------------------------------- #
class EncargadoCreateView(CreateView):
    model = Persona
    form_class = EncargadorForm
    template_name = 'encargado_form.html'
    success_url = reverse_lazy('alquiler:encargado_listar')
    title = "Alta de encargado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        if existe_persona_activa(self, dni):
            mensaje_error(self.request, f'{MSJ_PERSONA_EXISTE}')
            form = EncargadorForm(self.request.POST)
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
                es_encargado = True
            )
            persona.save()

            current_datetime = timezone.now()

            encargado = Encargado(
                persona=persona,
                tipo = Encargado.TIPO,
                desde = current_datetime,
            )
            encargado.save()
            mensaje_exito(self.request, f'{MSJ_CORRECTO_ALTA_AFILIADO}')
            return redirect('alquiler:encargado_listar')

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

from django.db.models import Q

# ----------------------------- LISTADO DE ENCARGADO  ----------------------------------- #
class EncargadoListView(ListFilterView):
    model = Encargado
    filter_class = EncargadoFilterForm
    template_name = 'encargado_listar.html'
    paginate_by = MAXIMO_PAGINATOR
    success_url = reverse_lazy('alquiler:encargado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Encargados"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = EncargadoFilterForm(self.request.GET)
        if form.is_valid():
            persona_dni = form.cleaned_data.get('persona__dni')
            persona_apellido = form.cleaned_data.get('persona__apellido')

            if persona_dni:
                queryset = queryset.filter(persona__dni=persona_dni)
            if persona_apellido:
                queryset = queryset.filter(persona__apellido=persona_apellido)
        return queryset

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Encargado":
            return reverse_lazy('alquiler:encargado_alta', args=[self.object.pk])
        return super().get_success_url()


class EncargadoDetailView(DetailView):
    model = Encargado
    template_name = 'encargado_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle del Encargado"
        return context


class EncargadoUpdateView(UpdateView):
    model = Encargado
    form_class = EncargadoUpdateForm
    template_name = 'encargado_form.html'  
    success_url = reverse_lazy('cursos:profesor_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Profesor"
        return context

    def form_valid(self, form):
        mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

# ----------------------------- CREATE DE SERVICIO  ----------------------------------- #
class GestionServicioView(CreateView, ListView):
    model = Servicio
    template_name = 'gestion_servicio.html'  
    form_class = ServiciorForm
    paginate_by = MAXIMO_PAGINATOR
    context_object_name = 'servicios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Gestión de Servicio"
        context['form'] = self.get_form()
        context['filtros'] = ServicioFilterForm()
        return context

    def get_success_url(self):
        return reverse_lazy('alquiler:gestion_servicio')
    
    def form_valid(self, form):
        form.instance.nombre = form.cleaned_data['nombre'].title()
        mensaje_exito(self.request, f'{MSJ_SERVICIO_ALTA_EXITOSA}')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_TIPO_NUMERO_EXISTE}')
        return redirect('cursos:gestion_servicio')
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener los filtros del formulario
        filter_form = ServicioFilterForm(self.request.GET)
        if filter_form.is_valid():
            nombre_filter = filter_form.cleaned_data.get('nombre')
            if nombre_filter:
                queryset = queryset.filter(nombre__icontains=nombre_filter)
        return queryset.order_by('nombre')



class ServicioDetailView(DetailView):
    model = Servicio
    template_name = "servicio_detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Servicio'
        return context
    

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServiciorForm
    template_name = 'Servicio_form.html'
    success_url = reverse_lazy('alquiler:gestion_servicio')
    title = "Formulario Alta de Servicio"  # Agrega un título

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de servicio exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)
    
class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServiciorForm
    template_name = 'Servicio_form.html'
    success_url = reverse_lazy('alquiler:gestion_servicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Servicio"
        return context

    def form_valid(self, form):
        actividad = form.save()
        mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
        return redirect('alquiler:gestion_servicio')

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_NOMBRE_EXISTE}')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

# ----------------------------- LISTADO DE SERVICIO  ----------------------------------- #
class ServiciosListView(ListFilterView):
    model = Servicio
    paginate_by = 100
    filter_class = ServicioFilterForm
    success_url = reverse_lazy('alquiler:servicio_listar')
    template_name = 'servicio_listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Servicios"
        return context

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Servicio":
            return reverse_lazy('alquiler:servicio_crear', args=[self.object.pk])
        return super().get_success_url()            

# ----------------------------- CREATE DE SALON  ----------------------------------- #
class SalonCreateView(CreateView):
    model = Salon
    form_class = SalonrForm
    template_name = 'salon_form.html'
    success_url = reverse_lazy('alquiler:salon_crear')
    title = "Formulario de Salón"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title
        context['servicios'] = Servicio.objects.all()
        
        #Rol de encargado que no tienen fecha fin
        encargados = Rol.objects.all().filter(tipo=ROL_TIPO_ENCARGADO, hasta__isnull=True)
        context['encargados'] = encargados
        return context

    def form_valid(self, form):
        encargado_id = self.request.POST.get('enc_encargado')
        if encargado_id == '0':
            mensaje_advertencia(self.request, f'Seleccione al encargado')
            return super().form_invalid(form)
        
        rol = get_object_or_404(Encargado, persona=encargado_id)
        encargado = get_object_or_404(Encargado, persona=rol.persona)
        
        form.instance.encargado = encargado
        form.save()

        mensaje_exito(self.request, f'{MSJ_CORRECTO_ALTA_SALON}')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_CORRECTION}')
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
class SalonesListView(ListFilterView):
    model = Salon
    filter_class = SalonFilterForm
    template_name = 'salon_list.html'
    paginate_by = MAXIMO_PAGINATOR
    success_url = reverse_lazy('alquiler:salon_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Salones"
        return context

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Salon":
            return reverse_lazy('alquiler:salon_crear', args=[self.object.pk])
        return super().get_success_url()        
    

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
    

# ----------------------------- CREATE DE ALQUILER  ----------------------------------- #

class AlquilerCreateView(CreateView):
    model = Alquiler
    form_class = AlquilerForm
    template_name = 'alquiler_form.html'
    success_url = reverse_lazy('alquiler:pagar_alquiler_crear')
    title = "Alquiler de Salón"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        salon = form.cleaned_data["salon"]
        fecha = form.cleaned_data["fecha_alquiler"]
        turno = form.cleaned_data["turno"]
        alquiler = Alquiler.objects.first()
        print("ALQUILER EXISTENTE", alquiler)
        if alquiler is not None:
            if alquiler.verificar_existencia_alquiler(salon, fecha, turno):
                #el alquiler ya existe
                messages.error(self.request, f'{ICON_ERROR} Ya existía un alquiler del salón {salon} en la fecha {fecha} en el turno {turno}.')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                #el alquiler no exite y se puede alquilar. Guardar el nuevo alquiler
                messages.success(self.request, f'{ICON_CHECK} Alquiler exitosa!')
                return super().form_valid(form)
        else: 
            # es el primer alquiler y se guarda
            messages.success(self.request, f'{ICON_CHECK} Alquiler creado con éxito!')
            return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)
    


# ----------------------------- LIST DE ALQUILER  ----------------------------------- #
class AlquilieresListView(ListFilterView):
    model = Alquiler
    paginate_by = MAXIMO_PAGINATOR
    filter_class = AlquilerFilterForm
    success_url = reverse_lazy('alquiler:alquiler_listar')
    template_name = 'alquiler_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['titulo'] = "Listado de Alquileres"
        return context
    
    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Alquiler":
            return reverse_lazy('alquiler:alquiler_crear', args=[self.object.pk])
        return super().get_success_url()    
    
    def alquiler_confirm_delete (request, pk):
        alquiler = Alquiler.objects.get(pk=pk)
        return render (request,'alquileres/alquiler_confirm_delete.html',{'alquiler':alquiler})


# ----------------------------- DETAIL DE ALQUILER  ----------------------------------- #
class AlquilerDetailView (DetailView):
    model = Alquiler
    template_name = 'alquiler_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle de alquiler"
        return context
    

# ----------------------------- CREATE DE PAGO  ----------------------------------- #

class PagoAlquilerCreateView(CreateView):
    model = Pago_alquiler
    form_class = PagoForm
    template_name = 'pago_form.html'
    success_url = reverse_lazy('alquiler:alquiler_listar')
    title = "Formulario Alta de Pago"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        alquileres_sin_pagos = Pago_alquiler.alquileres_sin_pago  # Obtener todos los alquileres sin pago
        context['alquileres_sin_pagos'] = alquileres_sin_pagos  # Pasarlos al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de pago exitosa!')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)