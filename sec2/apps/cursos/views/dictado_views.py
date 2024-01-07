from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
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

##--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_form.html'
    success_url = reverse_lazy('cursos:dictado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, id=self.kwargs.get('pk'))
        context['titulo'] = f"Dictado para el curso {context['curso'].nombre}"
        context['profesor_form'] = ProfesorForm()
        return context

    def form_valid(self, form):

        # Obtén el curso asociado al dictado
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk'))
        
        # Guarda el dictado en la base de datos sin commit
        dictado = form.save(commit=False)
        
        if  dictado.maximos_alumnos > curso.capacidad_maxima:
            messages.error(self.request, 'Máximo de inscriptos supera la capacidad máxima del curso.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        
        dictado.curso = curso  # Asigna el curso al dictado

        # Obtén el curso asociado al dictado
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk'))
        
        # Guarda el dictado en la base de datos sin commit
        dictado = form.save(commit=False)
        dictado.curso = curso  # Asigna el curso al dictado
        
        # Verifica la validez del formulario
        if not form.is_valid():
            return self.form_invalid(form)

        # Guarda el dictado en la base de datos
        dictado.save()

        # Crea la relación Titular
        profesor_id = self.request.POST.get('profesor')
        profesor = get_object_or_404(Profesor, id=profesor_id)
        Titular.objects.create(profesor=profesor, dictado=dictado)

        messages.success(self.request, 'Dictado creado exitosamente. Recargue la página del detalle del curso')

        # Redirige a la vista de detalle del curso
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cursos:dictado_detalle', args=[self.object.curso.pk, self.object.pk])

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION}')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
##--------------- DICTADO DETALLE --------------------------------
class DictadoDetailView(DetailView):
    model = Dictado
    template_name = 'dictado/dictado_detail.html'
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return Dictado.objects.get(curso__pk=curso_pk, pk=dictado_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = Curso.objects.get(id=self.kwargs.get('curso_pk'))
        context['titulo'] = "Detalle del dictado"
        context['tituloListado'] = 'Clases Asociadas'
        # Obtener el nombre del profesor asociado al dictado
        titular = self.get_titular(context['object'])
        context['nombre_profesor'] = (
            f"{titular.profesor.persona.nombre}, "
            f"{titular.profesor.persona.apellido}"
        ) if titular else "Sin titular"

        # Obtener todas las clases asociadas al dictado
        clases = Clase.objects.filter(dictado=context['object'])
        context['clases'] = clases

        return context

    def get_titular(self, dictado):
        try:
            titular = dictado.titular_set.get()  # Acceder al titular asociado al dictado
            return titular
        except Titular.DoesNotExist:
            return None

##--------------- DICTADO UPDATE --------------------------------
class DictadoUpdateView(UpdateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Detalle"
        return context
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dictado = self.get_object()
        # Asegúrate de que el objeto Dictado tenga un Titular asociado
        titular = self.get_titular(dictado)
        if titular:
            # Si hay un Titular asociado, establece el valor del profesor en el formulario
            form.fields['profesor'].initial = titular.profesor.id
        return form

    def get_success_url(self):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.object.pk  # Accede al ID del dictado actualizado
        return reverse_lazy('cursos:dictado_detalle', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})

    def get_titular(self, dictado):
        try:
            # Intenta obtener el Titular asociado al Dictado
            titular = Titular.objects.get(dictado=dictado)
            return titular
        except Titular.DoesNotExist:
            # En caso de que no exista Titular, devuelve None
            return None

    def form_valid(self, form):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_pk'))
        dictado = form.save(commit=False)
        dictado.curso = curso

        # Obtén el profesor seleccionado en el formulario
        profesor_id = self.request.POST.get('profesor')
        profesor = get_object_or_404(Profesor, id=profesor_id)

        # Actualiza o crea el titular asociado al dictado con el nuevo profesor
        titular, created = Titular.objects.get_or_create(dictado=dictado, defaults={'profesor': profesor})
        if not created:
            titular.profesor = profesor
            titular.save()
        messages.success(self.request, 'Dictado modificado exitosamente.')
        return super().form_valid(form)

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