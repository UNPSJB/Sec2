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

    def get_success_url(self):
        return reverse_lazy(
            "cursos:dictado_detalle",
            kwargs={
                "curso_pk": self.kwargs["curso_pk"],
                "dictado_pk": self.kwargs["dictado_pk"],
            },
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Obtiene el dictado relacionado con el horario
        dictado_id = self.kwargs["dictado_pk"]
        dictado = get_object_or_404(Dictado, pk=dictado_id)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Nuevo horario"
        return context

    def form_valid(self, form):
        # Obtiene la clase relacionada con el dictado
        dictado_id = self.kwargs["dictado_pk"]
        dictado = get_object_or_404(Dictado, pk=dictado_id)
        # Asigna el dictado a la clase antes de guardarla
        form.instance.dictado = dictado
        # Guarda la clase para obtener el ID asignado
        response = super().form_valid(form)
        messages.success(self.request, f'{ICON_CHECK} Modificación exitosa!')
        return response