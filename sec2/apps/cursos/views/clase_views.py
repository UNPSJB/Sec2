from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import Dictado, Aula, Clase
from ..forms.clase_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

##--------------- CREACION DE CLASE --------------------------------
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clase/clase_form.html'
    success_url = reverse_lazy('cursos:index')

    #[FALTA] controlar que la cantidad de clases no supere la cantidad de clases maximas aproximadas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de Clases"
        return context

    def form_valid(self, form):
        # Obtén el dictado relacionado con la clase
        dictado_id = self.kwargs['dictado_pk']
        dictado = get_object_or_404(Dictado, pk=dictado_id)

        # Asigna el dictado a la clase antes de guardarla
        form.instance.dictado = dictado

        # Guarda la clase para obtener el ID asignado
        response = super().form_valid(form)

        # Asigna los horarios seleccionados a la clase
        form.instance.horarios.set(form.cleaned_data['horarios'])

        return response

##--------------- CLASE DETALLE --------------------------------
class ClaseDetailView(DetailView):
    model = Clase
    template_name = 'clase/clase_detail.html'
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        clase_pk = self.kwargs.get('clase_pk')
        return get_object_or_404(Clase, dictado__curso__pk=curso_pk, dictado__pk=dictado_pk, pk=clase_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dictado'] = get_object_or_404(Dictado, id=self.kwargs.get('dictado_pk'))
        context['clase'] = Clase.objects.get(id=self.kwargs.get('dictado_pk'))
        context['titulo'] = "Detalle de la clase    "
        context['tituloListado'] = 'Horario Asociadas'
        # Obtener todas las clases asociadas al dictado
        # clases = Clase.objects.filter(dictado=context['object'])
        # context['dictado'] = clases

        return context

class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm
