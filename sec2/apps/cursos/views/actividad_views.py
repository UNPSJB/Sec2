from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from ..models import Actividad
from ..forms.actividad_forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView

## ------------  CREATE AND LIST ACTIVIDAD -------------------
class ActividadCreateListView(CreateView, ListView):
    model = Actividad
    template_name = 'actividad/actividad_alta_listado.html'
    form_class = ActividadForm
    context_object_name = 'actividades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Gestión de Actividad"
        context['form'] = self.get_form()
        context['actividades'] = self.get_queryset()  # Use filtered queryset
        context['filtros'] = ActividadFilterForm()
        return context

    def get_success_url(self):
        return reverse_lazy('cursos:actividad')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.nombre = form.cleaned_data['nombre'].title()
        form.save()
        messages.success(self.request, 'Alta de actividad exitosa!')
        return response
    
    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} El nombre ya existe o posee caracteres no deseados.')
        return redirect('cursos:actividad')

    def get(self, request, *args, **kwargs):
        # Asegúrate de que el queryset esté disponible antes de llamar a super().get()
        self.object_list = self.get_queryset()
        return super(CreateView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        # Default queryset, puedes ajustarlo según tus necesidades
        queryset = Actividad.objects.all()

        # Obtén el formulario de filtro de la solicitud
        filter_form = ActividadFilterForm(self.request.GET)

        # Verifica si el formulario es válido y aplica los filtros
        if filter_form.is_valid():
            # Ejemplo: Filtrar según el campo 'nombre'
            nombre_filter = filter_form.cleaned_data.get('nombre')
            if nombre_filter:
                # Coincidencia parcial insensible a mayúsculas y minúsculas para 'nombre'
                queryset = queryset.filter(nombre__icontains=nombre_filter)

            # Agrega más filtros según los campos de tu formulario

        # Imprime el queryset para depurar
        print("Queryset:", queryset)

        return queryset    

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
    success_url = reverse_lazy('cursos:actividad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Actividad"
        return context

    def form_valid(self, form):
        actividad = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Actividad modificado con éxito')
        return redirect('cursos:actividad_detalle', pk=actividad.pk)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

# ## ------------ ACTIVIDAD DELETE -------------------
def actividad_eliminar(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    try:
        actividad.delete()
        messages.success(request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> La actividad se eliminó correctamente.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar la actividad.')
    return redirect('cursos:actividad')