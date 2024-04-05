from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from utils.funciones import mensaje_advertencia, mensaje_exito
from ..models import Aula, Reserva
from ..forms.aula_forms import *
from django.urls import reverse_lazy
from django.contrib import messages

## ------------  CREATE AND LIST AULA -------------------
class GestionAulaView(CreateView, ListView):
    model = Aula
    template_name = 'aula/gestion_aula.html'  
    form_class = AulaForm
    paginate_by = MAXIMO_PAGINATOR
    context_object_name = 'aulas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Gestión de Aula"
        context['form'] = self.get_form()
        context['aulas'] = self.get_queryset()  # Use filtered queryset
        context['filtros'] = AulaFilterForm()
        return context

    def get_success_url(self):
        return reverse_lazy('cursos:gestion_aula')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        mensaje_exito(self.request, f'{MSJ_AULA_ALTA_EXITOSA}')
        return response
    
    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_TIPO_NUMERO_EXISTE}')
        return redirect('cursos:gestion_aula')
    
    def get(self, request, *args, **kwargs):
        # Asegúrate de que el queryset esté disponible antes de llamar a super().get()
        self.object_list = self.get_queryset()
        return super(CreateView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Aula.objects.all()
        # Obtener los filtros del formulario
        filter_form = AulaFilterForm(self.request.GET)
        if filter_form.is_valid():
            capacidad = filter_form.cleaned_data.get('capacidad')
            tipo = filter_form.cleaned_data.get('tipo')
            # Aplicar filtros según sea necesario
            if capacidad:
                queryset = queryset.filter(capacidad__lte=capacidad)
            if tipo:
                queryset = queryset.filter(tipo=tipo)
        # Ordenar de forma descendente por tipo y luego por número
        queryset = queryset.order_by('-tipo', 'numero')
        return queryset

## ------------ ACTIVIDAD DETALLE -------------------
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class AulaDetailView(DetailView):
    model = Aula
    template_name = "aula/aula_detalle.html"
    paginate_by = MAXIMO_PAGINATOR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aula = self.object
        current_date = date.today()  # Get the current date
        
        reservas = Reserva.objects.filter(aula=aula, fecha__gte=current_date).order_by('fecha', 'horario__hora_inicio')
        
        # Configurar la paginación
        paginator = Paginator(reservas, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            reservas = paginator.page(page)
        except PageNotAnInteger:
            reservas = paginator.page(1)
        except EmptyPage:
            reservas = paginator.page(paginator.num_pages)

        context['reservas'] = reservas

        context['titulo'] = 'Detalle de Aula'
        context['tituloListado'] = 'Proximas reservas del aula'
        return context

## ------------ UPDATE -------------------
class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula/aula_alta.html'
    context_object_name = 'aula'
    success_url = reverse_lazy('cursos:gestion_actividad')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Aula"
        context['filtros'] = AulaFilterForm()
        return context

    def form_valid(self, form):
        aula = form.save()
        messages.success(self.request, f'{ICON_CHECK} Aula modificado con éxito')
        return redirect('cursos:aula_detalle', pk=aula.pk)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Atencion:')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

## ------------ ELIMINAR -------------------
def aula_eliminar(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    try:
        aula.delete()
        messages.success(request, f'{ICON_CHECK} El aula se eliminó correctamente!')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar el aula.')
    return redirect('cursos:gestion_aula')