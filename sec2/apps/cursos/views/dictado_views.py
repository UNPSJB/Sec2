from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Curso, Dictado, Titular, Horario
from utils.constants import *
from django.shortcuts import render
from django.urls import reverse
from ..forms.dictado_forms import *
from ..forms.profesor_forms import ProfesorForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from datetime import timedelta


#--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_alta.html'
    success_url = reverse_lazy('cursos:curso_detalle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, id=self.kwargs.get('pk'))
        context['titulo'] = f"Dictado para {context['curso'].nombre}"
        context['profesor_form'] = ProfesorForm()
        return context

    def form_valid(self, form):
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

        # Obtiene la fecha de inicio del dictado
        fecha_inicio = dictado.fecha

        # Crea el horario para el día de la semana de la fecha de inicio
        dia_semana_inicio = fecha_inicio.weekday()  

        # Crea la instancia de Horario
        horario = Horario(
            dia_semana=dia_semana_inicio,
            hora_inicio=fecha_inicio.time(),  # Puedes ajustar según tus necesidades
            dictado=dictado,
        )

        horario.clean()
        # Guarda el horario en la base de datos
        horario.save()
        # Si la hora_fin está nula, asigna la hora de fin al horario usando el método clean
        messages.success(self.request, 'Dictado creado exitosamente')

        # Redirige a la vista de detalle del curso
        return super().form_valid(form)
        messages.success(self.request, 'Dictado creado exitosamente')

        # Redirige a la vista de detalle del curso
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('cursos:curso_detalle', args=[self.object.curso.pk])

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION} {form.errors}')
        context = self.get_context_data()
        print("Errores del formulario:", form.errors)
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
        dictado = self.object  # El objeto de dictado obtenido de la vista

        context['titulo'] = "Detalle del dictado"
        context['tituloListado'] = 'Clases Asociadas'

        # Obtener todas las clases asociadas al dictado a través de los horarios
        # clases = Clase.objects.filter(horario__dictado=dictado)
        # context['clases'] = clases

        context['curso'] = Curso.objects.get(id=self.kwargs.get('curso_pk'))
        # Obtener todos los horarios asociados al dictado
        horarios = dictado.horarios.all()
        context['horarios'] = horarios

        # Obtener el nombre del profesor asociado al dictado
        titular = self.get_titular(context['object'])
        context['nombre_profesor'] = (
            f"{titular.profesor.persona.nombre}, "
            f"{titular.profesor.persona.apellido}"
        ) if titular else "Sin titular"
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
    template_name = 'dictado/dictado_alta.html'

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

# ##--------------- DICTADO LIST VIEW --------------------------------
# class DictadoListView(ListView):
#     model = Dictado
#     paginate_by = 100
#     filter_class = DictadoFilterForm
#     template_name = 'dictado/dictado_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         curso = Curso.objects.get(id=self.kwargs.get('pk'))
#         context['titulo'] = f"Listado de dictado para {curso.nombre}"
#         context["curso"] = self.kwargs['pk']
#         return context

#     def get_queryset(self):
#         dictados = super().get_queryset().filter(curso__pk=self.kwargs['pk'])

#         # Agregar información del titular para cada dictado
#         for dictado in dictados:
#             titular = self.get_titular(dictado)
#             dictado.titular = titular
#         return dictados

#     def get_titular(self, dictado):
#         try:
#             titular = Titular.objects.get(dictado=dictado)
#             return titular.profesor
#         except Titular.DoesNotExist:
#             return None