from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from utils.funciones import mensaje_advertencia, mensaje_error, mensaje_exito
from ..models import Actividad
from ..forms.actividad_forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView

## ------------  CREATE AND LIST ACTIVIDAD -------------------
class GestionActividadView(CreateView, ListView):
    model = Actividad
    template_name = 'actividad/gestion_actividad.html'
    form_class = ActividadForm
    paginate_by = MAXIMO_PAGINATOR
    context_object_name = 'actividades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Gestión de Actividad"
        context['form'] = self.get_form()
        context['filtros'] = ActividadFilterForm()
        return context

    def get_success_url(self):
        return reverse_lazy('cursos:gestion_actividad')

    def form_valid(self, form):
        form.instance.nombre = form.cleaned_data['nombre'].title()
        mensaje_exito(self.request, f'{MSJ_ACTIVIDAD_ALTA_EXITOSA}')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_NOMBRE_EXISTE}')
        return redirect('cursos:gestion_actividad')

    def get_queryset(self):
        queryset = super().get_queryset()

        filter_form = ActividadFilterForm(self.request.GET)
        if filter_form.is_valid():
            nombre_filter = filter_form.cleaned_data.get('nombre')
            if nombre_filter:
                queryset = queryset.filter(nombre__icontains=nombre_filter)

        return queryset.order_by('nombre')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

## ------------ ACTIVIDAD DETALLE -------------------
class ActividadDetailView(DetailView):
    model = Actividad
    template_name = 'actividad/actividad_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Actividad'
        return context

## ------------ ACTIVIDAD UPDATE -------------------
class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/actividad_alta.html'
    success_url = reverse_lazy('cursos:gestion_actividad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Actividad"
        return context

    def form_valid(self, form):
        actividad = form.save()
        mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
        return redirect('cursos:actividad_detalle', pk=actividad.pk)

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_NOMBRE_EXISTE}')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

# ## ------------ ACTIVIDAD DELETE -------------------
def actividad_eliminar(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    try:
        actividad.delete()
        mensaje_exito(request, f'{MSJ_ACTIVIDAD_EXITO_BAJA}')
    except Exception as e:
        mensaje_error(request, f'{MSJ_ERROR_ELIMINAR}')
    return redirect('cursos:gestion_actividad')