from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import Dictado, Aula, Clase, Horario
from ..forms.clase_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

# --------------- CREACION DE CLASE --------------------------------
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clase/clase_form.html'
    success_url = reverse_lazy('cursos:aula_listado')

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
        dictado_id = self.kwargs.get("dictado_pk")
        dictado = get_object_or_404(Dictado, pk=dictado_id)
        # Filtra las aulas que tienen capacidad suficiente para el dictado
        # form.fields["aula"].queryset = Aula.objects.filter(capacidad__gte=dictado.cupo)
        # Obtener todos los horarios asociados al dictado
        horarios_dictado = Horario.objects.filter(dictado=dictado)
        # Pasar los horarios al formulario como contexto
        form.horarios_dictado = horarios_dictado
        return form

    def get_context_data(self, **kwargs):
        dictado_id = self.kwargs.get("dictado_pk")
        dictado = get_object_or_404(Dictado, id=dictado_id)
        # Obtener todos los horarios asociados al dictado
        # horarios_dictado = Horario.objects.filter(dictado=dictado)
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Alta de Clase"
        # context["aulas_disponibles"] = Aula().obtener_aulas_disponibles(dictado.cupo)
        # context["horarios_dictado"] = horarios_dictado
        return context

    def form_valid(self, form):
        dictado_id = self.kwargs["dictado_pk"]
        dictado = get_object_or_404(Dictado, pk=dictado_id)
        form.instance.dictado = dictado
        response = super().form_valid(form)
        messages.success(self.request, "Clase creada exitosamente.")
        return response


# --------------- CLASE DETALLE --------------------------------
class ClaseDetailView(DetailView):
    model = Clase
    template_name = "clase/clase_detail.html"

    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get("curso_pk")
        dictado_pk = self.kwargs.get("dictado_pk")
        clase_pk = self.kwargs.get("clase_pk")
        return get_object_or_404(
            Clase, dictado__curso__pk=curso_pk, dictado__pk=dictado_pk, pk=clase_pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dictado"] = get_object_or_404(
            Dictado, id=self.kwargs.get("dictado_pk")
        )
        context["clase"] = Clase.objects.get(id=self.kwargs.get("clase_pk"))
        context["titulo"] = "Detalle de clase"
        context["tituloListado"] = "Control de asistencia"
        # Obtener todos horarios asociadas a la clase
        horario = Horario.objects.filter(clase=context['object'])
        context['horarios'] = horario
        return context


class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm
