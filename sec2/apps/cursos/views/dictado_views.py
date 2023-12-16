from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from ..models import Curso, Profesor, Dictado, Clase, Titular
from utils.constants import *
from django.shortcuts import render
from django.urls import reverse
from ..forms.dictado_forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


####################### SECCION DE DICTADO #######################
##--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = FormularioDictado
    template_name = 'dictado/dictado_form.html'
    success_url = reverse_lazy('cursos:dictado_listado')

    def get_initial(self,*args, **kwargs):
        curso= Curso.objects.get(pk=self.kwargs.get("pk"))
        return {'curso':curso}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id = self.kwargs.get('pk'))
        context['curso'] = curso
        context['titulo'] = f"Alta de dictado para el curso {curso.nombre}"
        tiene_profesor = Profesor.objects.exists()
        context['tiene_profesor'] = tiene_profesor
        return context

    def get(self, request, *args, **kwargs):
        if Profesor.objects.exists():
            return super().get(request, *args, **kwargs)
        else:
            messages.warning(
                self.request, 
                '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Tienes que dar de alta a un profesor para poder crear un Dictado!'
            )
            return redirect('cursos:profesor_crear')
        
    def get_success_url(self):
        # Obtiene el pk del curso desde los kwargs de la vista
        pk_curso = self.kwargs.get('pk', None)
        # Construye la URL inversa con el pk del curso
        return reverse('cursos:dictados_listado', kwargs={'pk': pk_curso})

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