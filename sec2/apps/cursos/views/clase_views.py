from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import Dictado, Aula, Clase
from ..forms.clase_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404

##--------------- CREACION DE CLASE --------------------------------
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clase/clase_form.html'

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

        # Otros campos específicos de tu lógica
        form.instance.dias_semana = form.cleaned_data['dias_semana']
        form.instance.hora_inicio = form.cleaned_data['hora_inicio']
        form.instance.hora_fin = form.cleaned_data['hora_fin']

        # Lógica adicional según tus necesidades...

        return super().form_valid(form)

class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm
