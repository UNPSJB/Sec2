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
        context['titulo'] = f"Nueva clase para el dictado"
        return context

class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm
