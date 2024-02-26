from datetime import timedelta
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import AsistenciaProfesor, Clase, Dictado, Aula, Horario, Profesor, Reserva, Titular
from ..forms.clase_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# --------------- CREACION DE CLASE --------------------------------
def generar_clases(request, curso_pk, dictado_id):
    # Obtén el objeto Dictado
    dictado = get_object_or_404(Dictado, pk=dictado_id)

    # Obtén todas las reservas asociadas a ese dictado
    reservas = Reserva.objects.filter(horario__dictado=dictado)

    # Crea una instancia de Clase por cada reserva
    for reserva in reservas:
        Clase.objects.create(reserva=reserva)

    messages.success(request, f'{ICON_CHECK}  Se generaron las clases para el dictado')
    url_dictado_detalle = reverse('cursos:dictado_detalle', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_id})
    return redirect(url_dictado_detalle)

# --------------- CLASE DETALLE --------------------------------
class ClaseDetailView(DetailView):
    model = Clase
    template_name = "clase/clase_detail.html"

    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get("curso_pk")
        dictado_pk = self.kwargs.get("dictado_pk")
        clase_pk = self.kwargs.get("clase_pk")
        return get_object_or_404(
            Clase, reserva__horario__dictado__curso__pk=curso_pk, reserva__horario__dictado__pk=dictado_pk, pk=clase_pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = get_object_or_404(Dictado, id=self.kwargs.get("dictado_pk"))
        clase = Clase.objects.get(id=self.kwargs.get("clase_pk"))
        
        # Obtener la lista de alumnos inscritos en el dictado
        alumnos_inscritos = dictado.alumnos.all()
        
        alumnos_asistieron = clase.asistencia.all()

        # Obtener los titulares asociados al dictado de la clase
        titulares = Titular.objects.filter(dictado=dictado).select_related('profesor')

        # Obtener los profesores de AsistenciaProfesor que son titulares y tienen la clase
        profesores_asistieron = AsistenciaProfesor.objects.filter(clase=clase).values_list('profesor__id', flat=True)
        context["dictado"] = dictado
        context["clase"] = clase
        context["titulo"] = "Detalle de clase"
        context["tituloListado"] = "Asistencia"
        context["tituloListado1"] = "Alumnos"
        context["tituloListado2"] = "Profesor"
        context["alumnos_inscritos"] = alumnos_inscritos
        context["alumnos_asistieron"] = alumnos_asistieron
        context["profesores_asistieron"] = profesores_asistieron
        context["titulares"] = titulares
        return context

    def post(self, request, *args, **kwargs):
        clase = self.get_object()
        if not clase.asistencia_tomada:
            # Marcar la asistencia para todos los alumnos inscritos en el curso
            clase.asistencia.set(clase.reserva.horario.dictado.alumnos.all())
            clase.asistencia_tomada = True
            clase.save()
            # Puedes realizar otras acciones aquí, como guardar el registro en la base de datos
        return HttpResponseRedirect(self.request.path_info)
