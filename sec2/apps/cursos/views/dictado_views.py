from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from apps.afiliados.models import Afiliado, Familiar
from apps.personas.forms import PersonaForm

from apps.personas.models import Persona
from ..models import Actividad, Alumno, Clase, Curso, Dictado, Titular, Horario, Reserva
from utils.constants import *
from django.urls import reverse
from ..forms.dictado_forms import *
from ..forms.profesor_forms import ProfesorForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

#--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_alta.html'
    success_url = reverse_lazy('cursos:curso_detalle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, id=self.kwargs.get('pk'))
        context['titulo'] = f"Dictado para {context['curso'].nombre}"
        actividad_curso = context['curso'].actividad
        context['profesores_capacitados'] = Profesor.objects.filter(actividades=actividad_curso)
        return context

    def form_valid(self, form):
        # Obtén el curso asociado al dictado
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk'))

        # Guarda el dictado en la base de datos sin commit
        dictado = form.save(commit=False)
        dictado.curso = curso  # Asigna el curso al dictado

        # Verifica la validez del formulario
        if not form.is_valid():
            return self.form_invalid(form)

        if curso.es_convenio:
            dictado.asistencia_obligatoria = True
        # Guarda el dictado en la base de datos
        dictado.save()

        # Crea la relación Titular
        profesor_id = self.request.POST.get('profesor')
        profesor = get_object_or_404(Profesor, id=profesor_id)
        Titular.objects.create(profesor=profesor, dictado=dictado)

        # Obtiene la fecha de inicio del dictado
        fecha_inicio = dictado.fecha

        # Crea el horario para el día de la semana de la fecha de inicio
        dia_semana_inicio = fecha_inicio.weekday()  

        # Crea la instancia de Horario
        horario = Horario(
            dia_semana=dia_semana_inicio,
            hora_inicio=fecha_inicio.time(),  
            dictado=dictado,
            es_primer_horario=True,  # Establece es_primer_horario en True
        )

        horario.clean()
        # Guarda el horario en la base de datos
        horario.save()
        # Si la hora_fin está nula, asigna la hora de fin al horario usando el método clean
        messages.success(self.request, f'{ICON_CHECK} Dictado creado exitosamente')
        # Redirige a la vista de detalle del curso
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cursos:curso_detalle', args=[self.object.curso.pk])

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} {MSJ_CORRECTION}')
        context = self.get_context_data()
        print("Errores del formulario:", form.errors)
        return self.render_to_response(context)

##--------------- DICTADO DETALLE --------------------------------
from decimal import Decimal, getcontext
import math

class DictadoDetailView(DetailView):
    model = Dictado
    template_name = 'dictado/dictado_detail.html'
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        print(f'curso_pk: {curso_pk}, dictado_pk: {dictado_pk}')
        return Dictado.objects.get(curso__pk=curso_pk, pk=dictado_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = self.object  # El objeto de dictado obtenido de la vista
        
        context['titulo'] = "Detalle del dictado"
        context['tituloListado'] = 'Clases Asociadas'
        
        curso = Curso.objects.get(id=self.kwargs.get('curso_pk'))
        context['curso'] = curso

        # Obtener todos los horarios asociados al dictado
        horarios = dictado.horarios.all()
        context['horarios'] = horarios

        # Obtener el nombre del profesor asociado al dictado
        titular = self.get_titular(context['object'])
        context['nombre_profesor'] = (
            f"{titular.profesor.persona.nombre}, "
            f"{titular.profesor.persona.apellido}"
        ) if titular else "Sin titular"

        # Verificar si hay alguna reserva asociada al dictado
        hay_reserva = any(self.get_reserva(horario) for horario in context['horarios'])
        context['hay_reserva'] = hay_reserva

        # Agregar el campo 'reserva' al contexto para cada horario y verificar asignación de aula
        todos_los_horarios_con_aula = True  # Suponemos inicialmente que todos tienen aula
        for horario in context['horarios']:
            horario.reserva = self.get_reserva(horario)
            # Verificar si el horario tiene asignado un aula
            if horario.reserva is None:
                todos_los_horarios_con_aula = False

        context['todos_los_horarios_con_aula'] = todos_los_horarios_con_aula
        # Obtener todas las clases asociadas al dictado a través de los horarios
        clases = Clase.objects.filter(reserva__horario__dictado=dictado).order_by('reserva__fecha')
        context['clases'] = clases

        # OBTENGO A TODOS MIS ALUMNOS (Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
        afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
        familiares_inscritos = Familiar.objects.filter(dictados=dictado)    
        profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
        alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
        
        # Combino todos los objetos en una lista
        todos_inscritos = list(afiliado_inscritos) + list(familiares_inscritos) + list(profesores_inscritos) + list(alumnos_inscritos)

        # Ordeno la lista por DNI y Apellido
        todos_inscritos_sorted = sorted(todos_inscritos, key=lambda x: (x.persona.dni, x.persona.apellido))

        # Agrego la lista ordenada al contexto
        context['todos_inscritos_sorted'] = todos_inscritos_sorted
        context['afiliado_inscritos'] = afiliado_inscritos
        context['familiares_inscritos'] = familiares_inscritos
        context['profesores_inscritos'] = profesores_inscritos
        context['alumnos_inscritos'] = alumnos_inscritos
    
        # Calculo la suma total de inscritos
        total_inscritos = (
            afiliado_inscritos.count() +
            familiares_inscritos.count() +
            profesores_inscritos.count() +
            alumnos_inscritos.count()
        )

        context['total_inscritos'] = total_inscritos
        if curso.es_convenio:
            context['costo_parcial'] = 'Gratuito'
        else:
            if dictado.periodo_pago == 2:
                # PERIODO DE PAGO POR CLASE
                cantidad_clase = Decimal(curso.modulos_totales) / Decimal(dictado.modulos_por_clase)
                cantidad_clase = Decimal(math.ceil(cantidad_clase))
                result = round(curso.costo / cantidad_clase, 2)
                context['costo_parcial'] = f"${result} AR por {dictado.get_periodo_pago_display()}"
            else:
                # PERIODO DE PAGO POR MES
                if clases.exists():
                    # Obtén las fechas de la primera y última clase
                    primera_fecha_clase = clases.first().reserva.fecha
                    ultima_fecha_clase = clases.last().reserva.fecha
                    # Calcula la diferencia de tiempo entre la primera y última fecha de clases
                    diferencia_tiempo = ultima_fecha_clase - primera_fecha_clase
                    # Calcula el número de meses
                    meses_transcurridos = round(diferencia_tiempo.days / 30)  # Suponiendo 30 días por mes para simplificar
                    # Realiza el cálculo del costo basado en el número de meses
                    result = round(curso.costo / meses_transcurridos, 2)
                    context['costo_parcial'] = f"${result} AR por {dictado.get_periodo_pago_display()}"
                else:
                    context['costo_parcial'] = 'Primero tiene generar las clases'
        return context

    def get_reserva(self, horario):
        # Obtener todas las reservas asociadas al horario
        reservas = Reserva.objects.filter(horario=horario)
        
        if reservas.exists():
            return reservas.first()  # Puedes ajustar esto según tus necesidades
        else:
            return None
        

    def get_titular(self, dictado):
        try:
            titular = dictado.titular_set.get()  # Acceder al titular asociado al dictado
            return titular
        except Titular.DoesNotExist:
            return None

##--------------- DICTADO UPDATE --------------------------------
class DictadoUpdateView(UpdateView):
    model = Dictado
    form_class = DictadoForm
    template_name = 'dictado/dictado_alta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = self.object
        context['titulo'] = "Modificar Detalle"
        if dictado.fecha:
            context['tiene_fecha_cargada'] = True
        else:
            context['tiene_fecha_cargada'] = False
        actividad_curso = dictado.curso.actividad
        context['profesores_capacitados'] = Profesor.objects.filter(actividades=actividad_curso)
        return context
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dictado = self.get_object()
        # Asegúrate de que el objeto Dictado tenga un Titular asociado
        titular = self.get_titular(dictado)
        if titular:
            # Si hay un Titular asociado, establece el valor del profesor en el formulario
            form.fields['profesor'].initial = titular.profesor.id if titular.profesor else None
            # Si estás en la vista de actualización, haz que la fecha no sea editable
        return form

    def get_success_url(self):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.object.pk  # Accede al ID del dictado actualizado
        return reverse_lazy('cursos:dictado_detalle', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})

    def get_titular(self, dictado):
        try:
            # Intenta obtener el Titular asociado al Dictado
            titular = Titular.objects.get(dictado=dictado)
            return titular
        except Titular.DoesNotExist:
            # En caso de que no exista Titular, devuelve None
            return None

    def form_valid(self, form):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_pk'))
        dictado = form.save(commit=False)
        dictado.curso = curso

        # Obtén el profesor seleccionado en el formulario
        profesor_id = self.request.POST.get('profesor')
        profesor = get_object_or_404(Profesor, id=profesor_id)

        # Actualiza o crea el titular asociado al dictado con el nuevo profesor
        titular, created = Titular.objects.get_or_create(dictado=dictado, defaults={'profesor': profesor})
        if not created:
            titular.profesor = profesor
            titular.save()
        messages.success(self.request, f'{ICON_CHECK} Dictado modificado exitosamente.')
        return super().form_valid(form)

##--------------- DICTADO INSCRIPCIÓN --------------------------------
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

class BuscarPersonaView(View):

    def get(self, request, *args, **kwargs):
        dni = request.GET.get('dni', '')
        print("----------------------------------------------",dni)
        try:
            # FILTRA EL PRIMERO QUE ENCUENTRA POR QUE LO GUARDA DOS VECES EN LA BASE
            persona = Persona.objects.filter(dni=dni).first()
            if persona is not None:
                print("---------------SI EXISTE----------------------------:", persona)
                persona_data = {
                    'pk': persona.pk,
                    'dni': persona.dni,
                    'cuil': persona.cuil,
                    'nombre': persona.nombre,
                    'apellido': persona.apellido,
                    'fecha_nacimiento': persona.fecha_nacimiento,
                    'celular': persona.celular,
                    'direccion': persona.direccion,
                    'nacionalidad': persona.nacionalidad,
                    'mail': persona.mail,
                    'estado_civil': persona.estado_civil,
                    'es_afiliado': persona.es_afiliado,
                    'es_alumno': persona.es_alumno,
                    'es_profesor': persona.es_profesor,
                    'es_encargado': persona.es_encargado,
                    'es_grupo_familiar': persona.es_grupo_familiar,
                }

                return JsonResponse({'persona': persona_data})
            else:
                print("--------------PERSONA NO EXISTE--------------------------------",dni)
                return JsonResponse({'persona': None})
        except Persona.DoesNotExist:
            return JsonResponse({'persona': None})


class VerificarInscripcionView(View):
    template_name = 'dictado/dictado_inscripcion.html'  # La plantilla que mostrará el formulario de inscripción

    def get(self, request, *args, **kwargs):
        curso_pk = kwargs.get('curso_pk')
        dictado_pk = kwargs.get('dictado_pk')
        # Obtener el objeto Dictado o devolver un error 404 si no existe
        dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
        print("DICTADO: ", dictado.cupo)

        # OBTENGO A TODOS MIS ALUMNOS (Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
        afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
        familiares_inscritos = Familiar.objects.filter(dictados=dictado)    

        # Obtener el atributo persona de todos los familiares_inscritos
        personas_familiares_inscritos = familiares_inscritos.values_list('persona', flat=True)

        # Convertir el resultado en una lista si es necesario
        lista_personas_familiares_inscritos = list(personas_familiares_inscritos)

        # Imprimir o utilizar la lista según tus necesidades
        print(lista_personas_familiares_inscritos)

        print(familiares_inscritos)
        profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
        alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
        
        # Calculo la suma total de inscritos
        total_inscritos = (
            afiliado_inscritos.count() +
            familiares_inscritos.count() +
            profesores_inscritos.count() +
            alumnos_inscritos.count()
        )

        print("TOTAL INSCRIPTOS: ", total_inscritos)

        # Verificar si hay cupo
        hay_cupo = total_inscritos < dictado.cupo
        print("HAY CUPO: ", hay_cupo)

        # Inicializamos los ids como una lista vacía
        inscritos_ids = []
        # Agrega los IDs de afiliados, familiares, profesores, alumno
        inscritos_ids.extend(list(afiliado_inscritos.values_list('persona__pk', flat=True)))
        inscritos_ids.extend(list(familiares_inscritos.values_list('persona__pk', flat=True)))
        inscritos_ids.extend(list(profesores_inscritos.values_list('persona__pk', flat=True)))
        inscritos_ids.extend(list(alumnos_inscritos.values_list('persona__pk', flat=True)))

        context = {
            'titulo': 'Incripción',
            'curso_pk': curso_pk,
            'dictado_pk': dictado_pk,
            'hay_cupo': hay_cupo,
            'inscritos_ids': inscritos_ids,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        dni = request.POST.get('dni')
        nombre = request.POST.get('nombre')

        # Verificar si existe una persona con el DNI proporcionado
        persona_exists = Persona.objects.filter(dni=dni).exists()

        # Obtener las claves primarias del curso y del dictado
        curso_pk = kwargs.get('curso_pk')
        dictado_pk = kwargs.get('dictado_pk')
        # Agregar las variables de contexto para informar en el HTML
        context = {
            'persona_exists': persona_exists,
            'curso_pk': curso_pk,
            'dictado_pk': dictado_pk,
        }

        if persona_exists:
            print("PERSONA EXISTE")

        return render(request, self.template_name, context)


def listaEspera(request, curso_pk, dictado_pk ):
    # Obtener el objeto Dictado
    dictado = Dictado.objects.get(id=dictado_pk)

    # Obtener todos los alumnos en lista de espera para el dictado
    alumnos_lista_espera = Alumno.objects.filter(lista_espera=dictado)
    print(alumnos_lista_espera)

    alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
    cantidad_alumnos_inscritos = alumnos_inscritos.count()
    print("TOTAL INSCRIPTOS: ", cantidad_alumnos_inscritos)
    hay_cupo = cantidad_alumnos_inscritos < dictado.cupo
    print("HAY CUPO: ", hay_cupo)


    titulo = 'Lista de espera'
    context = {
        'dictado': dictado,
        'alumnos_lista_espera': alumnos_lista_espera,
        'titulo': titulo,
        'hay_cupo': hay_cupo,
    }
    return render(request, 'dictado/dictado_lista_espera.html', context)


def sacarListaEspera(request, curso_pk, dictado_pk, alumno_pk):
    # Obtener el objeto Dictado
    dictado = Dictado.objects.get(id=dictado_pk)

    # Obtener el objeto Alumno en lista de espera
    alumno = get_object_or_404(Alumno, pk=alumno_pk, lista_espera=dictado)

    alumno.lista_espera.remove(dictado)
    alumno.dictados.add(dictado)
    messages.success(request, f'{ICON_CHECK} Alumno dado de alta correctamente en el dictado.')
    
    return redirect(reverse('cursos:dictado_lista_espera', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk}))


# ----------------- INSCRIPCION PARA EL AFILIADO -----------------
def inscribirAfiliado(request, curso_pk, dictado_pk, persona_pk):
    dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
    afiliado = get_object_or_404(Afiliado, persona__pk=persona_pk)

    afiliado.dictados.add(dictado)
    afiliado.persona.es_alumno = True
    afiliado.persona.save()
    afiliado.save()
    
    messages.success(request, f'{ICON_CHECK} Familiar inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
    return redirect(reverse('cursos:verificar_persona', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk}))

# ----------------- INSCRIPCION PARA EL GRUPO FAMILIAR -----------------
def inscribirFamiliar(request, curso_pk, dictado_pk, persona_pk):
    dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
    familiar = get_object_or_404(Familiar, persona__pk=persona_pk)

    familiar.dictados.add(dictado)
    familiar.persona.es_alumno = True
    familiar.persona.save()
    familiar.save()
    
    messages.success(request, f'{ICON_CHECK} Familiar inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
    return redirect(reverse('cursos:verificar_persona', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk}))

# ----------------- INSCRIPCION PARA EL PROFESOR COMO ALUMNO -----------------
def inscribirProfesor(request, curso_pk, dictado_pk, persona_pk):
    dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
    profesor = get_object_or_404(Profesor, persona__pk=persona_pk)
    
    # Verificar si existe un Titular con ese Profesor y ese Dictado
    titular_existente = Titular.objects.filter(profesor=profesor, dictado=dictado).exists()
    
    if titular_existente:
        messages.error(request, f'{ICON_ERROR} Error: El profesor a inscribir es titular del dictado.')
    else:
        profesor.dictados_inscriptos.add(dictado)
        profesor.persona.es_alumno = True
        profesor.persona.save()
        profesor.save()
        messages.success(request, f'{ICON_CHECK} Familiar inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')

    return redirect(reverse('cursos:verificar_persona', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk}))

# ----------------- INSCRIPCION PARA EL ALUMNO YA EXISTENTE-----------------
def inscribirAlumno(request, curso_pk, dictado_pk, persona_pk):
    dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
    alumno = get_object_or_404(Alumno, persona__pk=persona_pk)
    print(alumno)
    alumno.dictados.add(dictado)
    alumno.save()
    messages.success(request, f'{ICON_CHECK} Alumno inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
    return redirect(reverse('cursos:verificar_persona', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk}))