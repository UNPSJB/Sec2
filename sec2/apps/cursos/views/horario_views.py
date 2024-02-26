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
from django.utils.datetime_safe import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Q
import math

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

        # Obtener la hora de inicio del formulario
        hora_inicio_form = form.cleaned_data['hora_inicio']

        # Obtener el día de la semana del formulario
        dia_semana_form = form.cleaned_data['dia_semana']

        # Calcular la hora de fin utilizando la función calcular_hora_fin de la clase Horario
        hora_fin_calculada = Horario().calcular_hora_fin(hora_inicio_form, dictado.modulos_por_clase)

        # Obtener todos los horarios para el dictado y el mismo día de la semana
        horarios_existente = Horario.objects.filter(dictado=dictado, dia_semana=dia_semana_form)

        # Obtén el primer horario del dictado con es_primer_horario=True
        primer_horario = Horario.objects.filter(dictado=dictado, es_primer_horario=True).first()
        if primer_horario is not None:
            # Si el día de la semana es mayor, lanza el error de que no se puede
            #generar un horario antes que el de la fecha de inicio estipulada
            if dia_semana_form < primer_horario.dictado.fecha.weekday():
                messages.warning(self.request, f'{ICON_TRIANGLE} No se puede asignar un horario antes de la fecha de inicio estipulada')
                return self.form_invalid(form)
            elif dia_semana_form == primer_horario.dictado.fecha.weekday():
                # Verifica si el nuevo horario se encuentra antes del primer horario
                if form.instance.hora_inicio < primer_horario.hora_inicio:
                    messages.warning(self.request, f'{ICON_TRIANGLE} No se puede crear un horario antes del primer horario.')
                    return self.form_invalid(form)
                # Verificar si la hora de inicio está dentro del rango de algún horario existente
                for horario in horarios_existente:
                    if horario.hora_inicio is not None and horario.hora_fin is not None:
                        # Permitir que la hora de inicio sea igual a la hora de fin
                        if horario.hora_inicio <= hora_inicio_form < horario.hora_fin:
                            messages.warning(self.request, f'{ICON_TRIANGLE} Ya existe un horario el mismo día dentro del rango de horario.')
                            return self.form_invalid(form)
                        # Verificar si la hora_fin_calculada está dentro del rango de algún horario existente
                        if horario.hora_inicio < hora_fin_calculada <= horario.hora_fin:
                            messages.warning(self.request, f'{ICON_TRIANGLE} La hora de finalización del horario se superpone con otro horario existente.')
                            return self.form_invalid(form)

        # Asignar el valor calculado a la hora_fin del formulario
        form.instance.hora_fin = hora_fin_calculada
        
        # Asigna el dictado a la clase antes de guardarla
        form.instance.dictado = dictado
        # Guarda la clase para obtener el ID asignado
        response = super().form_valid(form)
        messages.success(self.request, f'{ICON_CHECK} Nuevo horario generado exitosamente!')
        return response

#-------------- ASIGNAR UN AULA ----------------------------------
def asignar_aula(request, curso_pk, dictado_pk, horario_id):
    titulo = 'Asignación de aula'
    
    # Obtener el horario y dictado asociado
    horario = get_object_or_404(Horario, id=horario_id)
    dictado = horario.dictado

    # Calcular la hora de inicio y fin del horario
    hora_inicio = horario.hora_inicio
    hora_fin = horario.hora_fin

    reservas = Reserva.objects.all()
  
    # Obtener las reservas que se superponen con el horario actual
    reservas_superpuestas = Reserva.objects.filter(
        Q(fecha=dictado.fecha) &
        Q(horario__hora_inicio__lt=hora_fin, horario__hora_fin__gt=hora_inicio)
    )

    # Obtener todas las aulas filtradas por tipo
    necesita_equipamento_informatico = horario.dictado.curso.requiere_equipamiento_informatico

    if necesita_equipamento_informatico:
        todas_aulas = Aula.objects.filter(tipo='computacion')
    else:
        todas_aulas = Aula.objects.filter(tipo='normal')

    # Obtener las aulas ocupadas en el horario actual
    aulas_ocupadas = reservas_superpuestas.values_list('aula', flat=True)

    # Obtener las aulas que no están ocupadas
    aulas_libres = todas_aulas.exclude(id__in=aulas_ocupadas)

    # Obtener las aulas disponibles que tienen capacidad para el cupo del dictado
    aulas_disponibles_con_capacidad = aulas_libres.filter(capacidad__gte=dictado.cupo)

    if not aulas_disponibles_con_capacidad.exists():
        return HttpResponse("No hay aulas disponibles.")
    
    modulos_totales = horario.dictado.curso.modulos_totales
    modulos_por_clase = horario.dictado.modulos_por_clase
    cantidad_clases = modulos_totales / modulos_por_clase

    horarios_relacionados = Horario.objects.filter(dictado=dictado)

    # Calcular la cantidad de clases por dictado y se redondea hacia arriba
    clases_por_dictado = cantidad_clases / horarios_relacionados.count()
    clases_por_dictado_redondeado = math.ceil(clases_por_dictado)

    # Obtener la fecha de inicio y fin del rango de fechas
    if horario.es_primer_horario: 
        fecha_inicio = horario.dictado.fecha
    else:
        fecha_inicio = calcular_fecha_inicio(horario)
            
    clases_por_dictado_redondeado = clases_por_dictado_redondeado - 1
    fecha_fin = fecha_inicio + timedelta(days=(7 * clases_por_dictado_redondeado ))
    
    # Filtrar las aulas disponibles en el rango de fecha y horario
    aulas_disponibles_en_rango = aulas_disponibles_con_capacidad.exclude(
        reservas__fecha__range=[fecha_inicio, fecha_fin],
        reservas__horario__dia_semana=horario.dia_semana,
        reservas__horario__hora_inicio__lt=horario.hora_fin,
        reservas__horario__hora_fin__gt=horario.hora_inicio
    )

    if request.method == 'POST':
        aula_seleccionada_id = request.POST.get('aula_seleccionada')
        aula_seleccionada = get_object_or_404(Aula, pk=aula_seleccionada_id)

        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            reserva, created = Reserva.objects.get_or_create(fecha=fecha_actual, horario=horario, aula=aula_seleccionada)
            fecha_actual += timedelta(days=7)  # Incrementar la fecha en una semana

        # Crear el objeto Reserva
        reserva.aula =  aula_seleccionada
        reserva.horario = horario
        reserva.save()

        # Actualizar el campo 'aula' en el objeto Horario
        horario.aula = aula_seleccionada
        horario.save()
        messages.success(request, f'{ICON_CHECK} Reservas generadas para el horario.')    
         # Redirigir a la vista dictado_detalle con los parámetros necesarios
        return redirect('cursos:dictado_detalle', curso_pk=horario.dictado.curso.pk, dictado_pk=horario.dictado.pk)
    else:
        # Verificar si ya existe una reserva para el horario actual
        reserva_existente = Reserva.objects.filter(horario=horario).first()

        if reserva_existente:
            return HttpResponse("El horario ya tiene una reserva con aula asignada.")
        
        return render(request, 'dictado/asignar_aula.html', {'aulas_disponibles': aulas_disponibles_en_rango, 'titulo' : titulo})

#-------------- CALCULA LA FECHA DE INICIO ----------------------------------
def calcular_fecha_inicio(horario):
    fecha_actual = horario.dictado.fecha
    dia_semana_horario = horario.dia_semana

    while fecha_actual.weekday() != dia_semana_horario:
        fecha_actual += timedelta(days=1)
    return fecha_actual
    """
    0: LUNES
    1: MARTES
    2. MIERCOLES
    3: JUEVES
    4: VIERNES
    5: SABADO
    6: DOMINGO
    """