from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from ..models import Curso, Profesor, Dictado, Clase, Titular
from utils.constants import *
from django.shortcuts import render
from django.urls import reverse
from ..forms.dictado_forms import *
from ..forms.profesor_forms import ProfesorForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


####################### SECCION DE DICTADO #######################
##--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_form.html'
    success_url = reverse_lazy('cursos:dictado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = Curso.objects.get(id=self.kwargs.get('pk'))
        context['titulo'] = f"Dictado para el curso {context['curso'].nombre}"
        context['profesor_form'] = ProfesorForm()  # Reemplaza ProfesorForm con el nombre real de tu formulario de profesor
        return context

    def form_valid(self, form):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk'))
        dictado = form.save(commit=False)
        dictado.curso = curso
        
        if form.is_valid():
            form_minimo_alumnos = form.cleaned_data.get('minimo_alumnos')
            form_maximos_alumnos = form.cleaned_data.get('maximos_alumnos')
            if form_minimo_alumnos >= form_maximos_alumnos:
                messages.error(self.request, 'El número mínimo de inscriptos debe ser menor que el máximo.')
                return self.form_invalid(form)
        
        dictado.save()

        # Crear la relación Titular
        profesor_id = self.request.POST.get('profesor')
        profesor = get_object_or_404(Profesor, id=profesor_id)
        Titular.objects.create(profesor=profesor, dictado=dictado)

        messages.success(self.request, 'Dictado creado exitosamente. Recargue la página del detalle del curso')

        context = self.get_context_data()
        return self.render_to_response(context)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION}')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context) 


##--------------- DICTADO DETALLE --------------------------------
class DictadoDetailView(DetailView):
    model = Dictado
    template_name = 'dictado/dictado_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el nombre del profesor asociado al dictado
        titular = self.get_titular(context['object'])
        context['nombre_profesor'] = (
            f"{titular.profesor.persona.nombre}, "
            f"{titular.profesor.persona.apellido}"
        ) if titular else "Sin titular"

        # Obtener todas las clases asociadas al dictado
        clases = Clase.objects.filter(dictado=context['object'])
        context['clases'] = clases

        context['titulo'] = "Dictado"
        return context

    def get_titular(self, dictado):
        try:
            titular = dictado.titular_set.get()  # Acceder al titular asociado al dictado
            return titular
        except Titular.DoesNotExist:
            return None

##--------------- DICTADO LIST VIEW --------------------------------
class DictadoListView(ListView):
    model = Dictado
    paginate_by = 100
    filter_class = DictadoFilterForm
    template_name = 'dictado/dictado_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id=self.kwargs.get('pk'))
        context['titulo'] = f"Listado de dictado para {curso.nombre}"
        context["curso"] = self.kwargs['pk']
        return context

    def get_queryset(self):
        dictados = super().get_queryset().filter(curso__pk=self.kwargs['pk'])

        # Agregar información del titular para cada dictado
        for dictado in dictados:
            titular = self.get_titular(dictado)
            dictado.titular = titular
        return dictados

    def get_titular(self, dictado):
        try:
            titular = Titular.objects.get(dictado=dictado)
            return titular.profesor
        except Titular.DoesNotExist:
            return None