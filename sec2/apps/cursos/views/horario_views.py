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

        # Obtener la hora de inicio del formulario
        hora_inicio_form = form.cleaned_data['hora_inicio']

        # Obtener el día de la semana del formulario
        dia_semana_form = form.cleaned_data['dia_semana']

        print("DÍA DE LA SEMANA")
        print(dia_semana_form)
        # Obtener todos los horarios para el dictado y el mismo día de la semana
        horarios_existente = Horario.objects.filter(dictado=dictado, dia_semana=dia_semana_form)
        print("HORARIO EXISTENTE")
        print(horarios_existente)
        # Verificar si la hora de inicio está dentro del rango de algún horario existente
        for horario in horarios_existente:
            print("")
            print("HORA DE INICIO")
            print(horario.hora_inicio)
            print("HORA INICIO FORM")
            print(hora_inicio_form)
            print("HORA FIN")
            print(horario.hora_fin)
            if horario.hora_inicio and horario.hora_fin:
                if horario.hora_inicio <= hora_inicio_form <= horario.hora_fin:
                    messages.warning(self.request, f'{ICON_TRIANGLE} Ya existe un horario el mismo día dentro del rango de horario.')
                    return self.form_invalid(form)
                    
        messages.warning(self.request, f'{ICON_TRIANGLE} SOY EL ELSE.')
        return self.form_invalid(form)


        # # Asigna el dictado a la clase antes de guardarla
        # form.instance.dictado = dictado
        # # Guarda la clase para obtener el ID asignado
        # response = super().form_valid(form)
        # messages.success(self.request, f'{ICON_CHECK} Modificación exitosa!')
        # return response

#-------------- ASIGNAR UN AULA ----------------------------------
from django.utils.datetime_safe import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Q

def asignar_aula(request, horario_id):
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

    # Obtener todas las aulas
    todas_aulas = Aula.objects.all()
    
    # Obtener las aulas ocupadas en el horario actual
    aulas_ocupadas = reservas_superpuestas.values_list('aula', flat=True)

    # Obtener las aulas que no están ocupadas
    aulas_libres = todas_aulas.exclude(id__in=aulas_ocupadas)

    # Obtener las aulas disponibles que tienen capacidad para el cupo del dictado
    aulas_disponibles_con_capacidad = aulas_libres.filter(capacidad__gte=dictado.cupo)

    # print("AULAS DISPONIBLES CON CAPACIDAD SUFICIENTE")
    # print(aulas_disponibles_con_capacidad)

    if not aulas_disponibles_con_capacidad.exists():
        return HttpResponse("No hay aulas disponibles.")
    else:
        print("AULAS DISPONIBLES")
        for aula in aulas_disponibles_con_capacidad:
            print(aula)

    modulos_totales = horario.dictado.curso.modulos_totales
    modulos_por_clase = horario.dictado.modulos_por_clase
    cantidad_clases = modulos_totales / modulos_por_clase


    """
    FALTA HACER LA LOGICA AL MOMENTO DE GENERAR EL HORARIO

    LOGICA HASTA AHORA
    Una vez presionado el boton de "Asignar Aula" mostrar un mensaje informando de que si desea asignar aula
    con un mensaje de advertencia informando que si desea asignar aulas ya no podrá generar más horarios.

    En el Asignar Aula se tendra que obtener todos los horarios asociados al dictado. Junto con la cantidad de clases.
    Se dividirá la cantidad de clases --> cantidad_clases / horarios asignados. De esta forma sé cuantas clases 
    se les asigna a cada ditado.

    """

    if request.method == 'POST':
        aula_seleccionada_id = request.POST.get('aula_seleccionada')
        aula_seleccionada = get_object_or_404(Aula, pk=aula_seleccionada_id)
        print("AULA SELECCIONADA")
        print(aula_seleccionada)
        # Crear el objeto Reserva
        reserva, created = Reserva.objects.get_or_create(fecha=horario.dictado.fecha)
        reserva.aula = aula_seleccionada
        reserva.horario = horario
        reserva.save()

        # Actualizar el campo 'aula' en el objeto Horario
        # horario.aula = aula_seleccionada
        # horario.save()
        print("RESERVA CREADA")
        print(reserva)
    else:
        # Obtener la fecha de inicio y fin del rango de fechas
        fecha_inicio = horario.dictado.fecha
        fecha_fin = fecha_inicio + timedelta(days=(7 * cantidad_clases))

        # Filtrar las aulas disponibles en el rango de fechas
        aulas_disponibles_en_rango = aulas_disponibles_con_capacidad.exclude(
            reservas__fecha__range=[fecha_inicio, fecha_fin]
        )

        # Filtrar las aulas disponibles por día y hora específicos
        aulas_disponibles_dia_hora = aulas_disponibles_en_rango.filter(
            reservas__fecha=fecha_inicio,
            horarios__dia_semana=horario.dia_semana,
            horarios__hora_inicio__lt=horario.hora_fin,
            horarios__hora_fin__gt=horario.hora_inicio
        )

        # Mostrar las aulas disponibles para el horario específico
        print("AULAS DISPONIBLES PARA EL HORARIO:")
        for aula in aulas_disponibles_dia_hora:
            print(aula)


        print("VERIFICAR SI YA TIENE UN AULA ASIGNADA")
        reserva_existente = Reserva.objects.filter(horario=horario).first()

        if reserva_existente:
            print("El horario ya tiene una reserva con aula asignada:", reserva_existente.aula)
            return HttpResponse("El horario ya tiene una reserva con aula asignada.")

    #     horario.aula = aula_seleccionada
    #     horario.save()
    #     print("FECHA DE INICIO")
    #     print(horario.dictado.fecha)
    #     # Agrega el horario directamente al campo 'horarios' de la instancia de Reserva
    #     reserva, created = Reserva.objects.get_or_create(fecha=horario.dictado.fecha)
    #     reserva.horarios.add(horario)

    # return render(request, 'dictado/asignar_aula.html', {'aulas_disponibles': aulas_disponibles})
    return render(request, 'dictado/asignar_aula.html', {'aulas_disponibles': aulas_disponibles_dia_hora})