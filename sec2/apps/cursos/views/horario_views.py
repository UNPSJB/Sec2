import datetime
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.contrib import messages
from ..models import Dictado, Horario, Aula, Reserva
from ..forms.clase_forms import *
from ..forms.horario_forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

#--------------- CREACION DE HORARIO --------------------------------
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

#-------------- ASIGNAR UN AULA ----------------------------------
from django.utils.datetime_safe import datetime
from datetime import timedelta
from django.http import HttpResponse

def asignar_aula(request, horario_id):
    titulo = 'Asignación de aula'
    horario = get_object_or_404(Horario, id=horario_id)
    modulo = horario.dictado.modulos_por_clase
    tiempo_modulo = timedelta(hours=modulo)
    hora_inicio_datetime = datetime.combine(datetime.today(), horario.hora_inicio)
    suma_resultado = hora_inicio_datetime + tiempo_modulo
    todos_los_horarios = Horario.objects.all()

    aulas_disponibles = Aula.objects.filter(capacidad__gte=horario.dictado.cupo)
    if not aulas_disponibles.exists():
        return HttpResponse("No hay aulas disponibles con capacidad suficiente para el dictado.")
    else:
        for aula in aulas_disponibles:
            print(aula)
            print("RESERVAS")
            print(aula.reservas.all())

    if request.method == 'POST':
        aula_seleccionada_id = request.POST.get('aula_seleccionada')
        aula_seleccionada = get_object_or_404(Aula, pk=aula_seleccionada_id)

        print("AULA SELECCIONADA")
        print(aula_seleccionada)
        # Asigna el aula al horario
        horario.aula = aula_seleccionada
        horario.save()
        print("FECHA DE INICIO")
        print(horario.dictado.fecha)
        # Agrega el horario directamente al campo 'horarios' de la instancia de Reserva
        reserva, created = Reserva.objects.get_or_create(fecha=horario.dictado.fecha)
        reserva.horarios.add(horario)

    return render(request, 'dictado/asignar_aula.html', {'horario': horario, 'aulas_disponibles': aulas_disponibles})