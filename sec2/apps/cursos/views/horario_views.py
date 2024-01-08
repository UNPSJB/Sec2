from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import Dictado, Aula, Clase, Horario
from ..forms.clase_forms import *
from ..forms.horario_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


##--------------- CREACION DE HORARIO --------------------------------
class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = "horario/horario_form.html"
    success_url = reverse_lazy('cursos:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Nuevo horario"
        return context

    def form_valid(self, form):
        # Obtiene la clase relacionada con el dictado
        clase_id = self.kwargs["clase_pk"]
        print("asdsadsad.------------asdasdasd")
        print(clase_id)
        clase = get_object_or_404(Clase, pk=clase_id)
        # Asigna el dictado a la clase antes de guardarla
        form.instance.clase = clase
        # Guarda la clase para obtener el ID asignado
        response = super().form_valid(form)
        # No es necesario asignar los horarios aquí si ya lo hiciste en el formulario
        return response