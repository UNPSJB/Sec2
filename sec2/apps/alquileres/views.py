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
    title = "Formulario Alta de Encargado"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        existing_person = Persona.objects.filter(dni=dni).first()

        if existing_person:
            messages.error(self.request, f'{ICON_ERROR} El encargado ya está registrada en el sistema.')
            form = EncargadorForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            encargado = Persona(
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
            encargado.save

            messages.success(self.request, f'{ICON_CHECK} Alta de encargado exitosa!')
            return redirect('alquiler:encargado_listar')


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

# ----------------------------- LISTADO DE ENCARGADO  ----------------------------------- #
class EncargadoListView(ListFilterView):
    model = Encargado
    paginate_by = 100
    filter_class = EncargadoFilterForm
    success_url = reverse_lazy('alquiler:encargado_listar')
    template_name = 'encargado_listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Encargados"
        return context

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Encargado":
            return reverse_lazy('alquiler:encargado_alta', args=[self.object.pk])
        return super().get_success_url()       


# ----------------------------- CREATE DE SERVICIO  ----------------------------------- #
class servicioCreateView(CreateView):
    model = Servicio
    form_class = ServiciorForm
    template_name = 'Servicio_form.html'
    success_url = reverse_lazy('alquiler:Servicio_form')
    title = "Formulario Alta de Servicio"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de servicio exitosa!')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
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
class SalonesListView(ListFilterView):
    model = Salon
    paginate_by = 100
    filter_class = SalonFilterForm
    success_url = reverse_lazy('alquiler:salon_listar')
    template_name = 'salon_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Salones"
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
    title = "Formulario de Alquiler de Salon"  # Agrega un título


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
        if alquiler.verificar_existencia_alquiler(salon, fecha, turno):
            #el alquiler ya existe
            messages.error(self.request, f'{ICON_ERROR} Ya existía un alquiler del salón {salon} en la fecha {fecha} en el turno {turno}.')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            #el alquiler no exite y se puede alquilar. Guardar el nuevo alquiler
            alquiler = Alquiler(
                afiliado=form.cleaned_data["afiliado"],
                salon=salon, 
                fecha_solicitud=datetime.now(),
                fecha_alquiler=fecha, 
                turno=turno,
                seguro = form.cleaned_data["seguro"],
                )
            alquiler.save()
            
            pago = Pago_alquiler( 
                alquiler=alquiler,
                fecha_pago=form.cleaned_data["fecha_pago"],
                forma_pago=form.cleaned_data["forma_pago"],
                )
            pago.save()
            #messages.success(self.request, f'{ICON_CHECK} Alquiler exitosa!')
            #return super().form_valid(form)
         
        # Redireccionar a la vista del detalle del salón con mensaje de éxito
        messages.success(self.request, f'{ICON_CHECK} Alquiler creado con éxito!')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)
    


def buscar_fechas_disponibles(request): 
    if request.method == 'POST':
        # Se obtienen los valores de afiliado y salón del formulario POST
        afiliado_id = request.POST['afiliado']
        salon_id = request.POST['salon']
        
        # Se obtienen las instancias de Afiliado y Salon a partir de los IDs
        afiliado = Afiliado.objects.get(id=afiliado_id)
        salon = Salon.objects.get(id=salon_id)
        
        # Se obtiene la fecha actual
        hoy = timezone.now().date()
        
        # Se filtran los alquileres del salón seleccionado y se ordenan por fecha de inicio
        alquileres = Alquiler.objects.filter(salon=salon, fecha_alquiler__isnull=True).order_by('fecha_inicio')
        
        # Lista para almacenar los alquileres disponibles
        available_alquileres = []

        for alquiler in alquileres:
            if alquiler.fecha_fin < hoy:
                continue
            elif alquiler.fecha_inicio <= hoy < alquiler.fecha_fin:
                available_alquileres.append(alquiler)
            else:
                break
        
        # Se renderiza la plantilla con la información recopilada
        return render(request, 'buscar_fechas_disponibles.html', {'afiliados': Afiliado.objects.all(), 'salones': Salon.objects.all(), 'afiliado': afiliado, 'salon': salon, 'available_dates': available_dates})
    else:
        # Se renderiza la plantilla con la lista completa de afiliados y salones si no se ha enviado un formulario POST
        return render(request, 'buscar_fechas_disponibles.html', {'afiliados': Afiliado.objects.all(), 'salones': Salon.objects.all()})

# ----------------------------- LIST DE ALQUILER  ----------------------------------- #
class AlquilieresListView(ListFilterView):
    model = Alquiler
    paginate_by = 100
    filter_class = AlquilerFilterForm
    success_url = reverse_lazy('alquiler:alquiler_listar')
    template_name = 'alquiler_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Alquileres"
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
        context['titulo'] = "Datos del alquiler"
        return context
    

# ----------------------------- CREATE DE PAGO  ----------------------------------- #

class PagoAlquilerCreateView(CreateView):
    model = Pago_alquiler
    form_class = PagoForm
    template_name = 'pago_form.html'
    success_url = reverse_lazy('alquiler:alquiler_list.html')
    title = "Formulario Alta de Pago"  # Agrega un título


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        return context

    
    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de pago exitosa!')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)