from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from utils.funciones import mensaje_advertencia, mensaje_error, mensaje_exito
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
    model = Persona
    form_class = ProfesorPersonaForm
    template_name = 'profesor/profesor_form.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ="Formulario de Profesor"
        context['actividades'] = Actividad.objects.all()  # Obtener todas las actividades
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        existing_person = Persona.objects.filter(dni=dni).first()
        if existing_person:
            mensaje_error(self.request, f'{MSJ_PERSONA_EXISTE}')
            form = ProfesorPersonaForm(self.request.POST)
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
                es_profesor = True
            )
            persona.save()

            # Guardar las actividades seleccionadas
            actividades_seleccionadas = self.request.POST.getlist('actividades')

            profesor = Profesor(persona=persona,
                                tipo = Profesor.TIPO
                                )
                
            profesor.ejerce_desde = form.cleaned_data["ejerce_desde"]
            # Profesor.register 
            profesor.save()

            profesor.actividades.set(actividades_seleccionadas)
            mensaje_exito(self.request, f'{MSJ_CORRECTO_ALTA_PROFESOR}')
            # Redirige al listado de profesores
            detail_url = reverse('cursos:profesor_listado')
            return redirect(detail_url)

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION}')
        return super().form_invalid(form)

## ------------------ DETALLE DE PROFESOR ------------------
class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'profesor/profesor_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle del Profesor"
        context['tituloListado'] = 'Titular'
        context['tituloDictadoInscrito'] = 'Dictados que esta inscrito como alumno'
        # Obtener el profesor actual
        profesor = self.object
        # Obtener todos los titulares asociados a este profesor
        titulares = Titular.objects.filter(profesor=profesor)
        context['titulares'] = titulares
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
        mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

## ------------------ LISTADO DE PROFESOR ------------------
class ProfesorListView(ListFilterView):
    model = Profesor
    paginate_by = MAXIMO_PAGINATOR
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

