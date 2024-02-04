from django.shortcuts import get_object_or_404, redirect
from ..models import Actividad, Profesor, Titular
from ..forms.profesor_forms import *
from django.views.generic import DetailView

from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView

from utils.constants import *
from sec2.utils import ListFilterView
from django.db import transaction

## ------------------ CREATE DE PROFESOR ------------------
class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = FormularioProfesor
    template_name = 'profesor/profesor_form.html'  
    success_url = reverse_lazy('cursos:profesor_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ="Alta de Profesor"
        context['actividades'] = Actividad.objects.all()  # Obtener todas las actividades
        return context

    def form_valid(self, form):
        with transaction.atomic():
            persona = Persona(
                dni=form.cleaned_data["dni"],
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

            # Guardar las actividades seleccionadas
            actividades_seleccionadas = self.request.POST.getlist('actividades')

            profesor = Profesor(persona=persona)
            profesor.ejerce_desde = form.cleaned_data["ejerce_desde"]
            profesor.save()
            profesor.actividades.set(actividades_seleccionadas)

        response = super().form_valid(form)
        # Mostrar el mensaje de éxito
        messages.success(self.request, f'{ICON_CHECK} Profesor dado de alta con éxito!')
        return response

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

## ------------------ DETALLE DE PROFESOR ------------------
class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'profesor/profesor_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Profesor"
        context['tituloListado'] = 'Dictados Asociados'
        return context

## ------------ PROFESOR UPDATE -------------------
class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorUpdateForm
    template_name = 'profesor/profesor_form.html'  
    success_url = reverse_lazy('cursos:profesor_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Profesor"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Profesor modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

## ------------------ LISTADO DE PROFESOR ------------------
class ProfesorListView(ListFilterView):
    model = Profesor
    paginate_by = 11
    filter_class = ProfesorFilterForm
    template_name = 'profesor/profesor_list.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = ProfesorFilterForm(self.request.GET)
        context['filtros'] = filter_form
        context['titulo'] = "Listado de profesores"
        return context

## ------------ ELIMINAR -------------------
def profesor_eliminar(request, pk):
    # profesor = get_object_or_404(Profesor, pk=pk)
    # try:
    #     profesor.delete()
    #     messages.success(request, f'{ICON_CHECK} El Profesor se eliminó correctamente!')
    # except Exception as e:
    #     messages.error(request, 'Ocurrió un error al intentar eliminar el aula.')
    return redirect('afiliados:funcionalidad_pendiente')
