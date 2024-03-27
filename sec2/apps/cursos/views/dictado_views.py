import json
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from apps.afiliados.models import Afiliado, Familiar
from apps.cursos.views.curso_views import obtenerUltimoDiaMesAnterior
from apps.personas.forms import PersonaForm

from apps.personas.models import Persona, Rol
from utils.funciones import mensaje_advertencia, mensaje_exito
from ..models import Actividad, Alumno, Clase, Curso, Dictado, ListaEspera, Titular, Horario, Reserva
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
        cupo_maximo = curso.cupo_estimativo
        

        # Guarda el dictado en la base de datos sin commit
        dictado = form.save(commit=False)

        if dictado.cupo_real > cupo_maximo:
            messages.warning(self.request, f'{ICON_TRIANGLE} El cupo supera el cupo maximo del dictado')
            return self.form_invalid(form)

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
        print("ESTOY AQUIII")
        context = self.get_context_data()
        print("Errores del formulario:", form.errors)
        return self.render_to_response(context)

##--------------- DICTADO DETALLE --------------------------------
from decimal import Decimal, getcontext
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class DictadoDetailView(DetailView):
    model = Dictado
    template_name = 'dictado/dictado_detail.html'
    paginate_by = MAXIMO_PAGINATOR
    
    def get_object(self, queryset=None):
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return Dictado.objects.get(curso__pk=curso_pk, pk=dictado_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        dictado = self.object  # El objeto de dictado obtenido de la vista
        
        context['titulo'] = "Detalle del dictado"
        context['tituloListado'] = 'Clases Asociadas'
        
        curso = Curso.objects.get(id=self.kwargs.get('curso_pk'))
        context['curso'] = curso

        # Obtener todos los horarios asociados al dictado
        horarios = dictado.horarios.all().order_by('dia_semana', 'hora_inicio')
    
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
        
        existen_clases =  clases.exists()

         # Configurar la paginación
        paginator = Paginator(clases, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            clases = paginator.page(page)
        except PageNotAnInteger:
            clases = paginator.page(1)
        except EmptyPage:
            clases = paginator.page(paginator.num_pages)
        
        context['clases'] = clases

        # OBTENGO A TODOS MIS ALUMNOS INSCRITOS(Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
        afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
        familiares_inscritos = Familiar.objects.filter(dictados=dictado)    
        profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
        alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
        
        # Combino todos los objetos en una lista
        # todos_inscritos = list(afiliado_inscritos) + list(profesores_inscritos) + list(alumnos_inscritos)
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
                result = round(curso.precio_total / cantidad_clase, 2)
                context['costo_parcial'] = f"${result} AR por {dictado.get_periodo_pago_display()}"
            else:
                # PERIODO DE PAGO POR MES
                # if not existen_clases:
                #     # Obtén las fechas de la primera y última clase
                #     primera_fecha_clase = clases.first().reserva.fecha
                #     ultima_fecha_clase = clases.last().reserva.fecha
                #     # Calcula la diferencia de tiempo entre la primera y última fecha de clases
                #     diferencia_tiempo = ultima_fecha_clase - primera_fecha_clase
                #     # Calcula el número de meses
                #     meses_transcurridos = round(diferencia_tiempo.days / 30)  # Suponiendo 30 días por mes para simplificar
                #     # Realiza el cálculo del costo basado en el número de meses
                #     result = round(curso.costo / meses_transcurridos, 2)
                #     context['costo_parcial'] = f"${result} AR por {dictado.get_periodo_pago_display()}"
                # else:
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
        id_rol = request.GET.get('id_rol', '')
        print("ID ROL: ",id_rol)
        try:
            # FILTRA EL PRIMERO QUE ENCUENTRA POR QUE LO GUARDA DOS VECES EN LA BASE
            rol = Rol.objects.filter(pk=id_rol).first()
            tipo_rol = rol.obtenerTipo()

            if rol is not None:
                rol_data = {
                    'pk': rol.pk,
                    'tipo_rol': tipo_rol,
                    'tipo': rol.tipo,
                    'persona': {
                        'pk': rol.persona.pk,
                        'dni': rol.persona.dni,
                        'cuil': rol.persona.cuil,
                        'nombre': rol.persona.nombre,
                        'apellido': rol.persona.apellido,
                        'fecha_nacimiento': rol.persona.fecha_nacimiento,
                        'celular': rol.persona.celular,
                        'direccion': rol.persona.direccion,
                        'nacionalidad': rol.persona.nacionalidad,
                        'mail': rol.persona.mail,
                        'estado_civil': rol.persona.estado_civil,
                        'es_afiliado': rol.persona.es_afiliado,
                        'es_alumno': rol.persona.es_alumno,
                        'es_profesor': rol.persona.es_profesor,
                        'es_encargado': rol.persona.es_encargado,
                        'es_grupo_familiar': rol.persona.es_grupo_familiar,
                    },
                }
                return JsonResponse({'rol': rol_data})
            else:
                return JsonResponse({'rol': None})
        except Persona.DoesNotExist:
            return JsonResponse({'rol': None})


class VerificarInscripcionView(View):
    template_name = 'curso/curso_inscripcion.html'  # La plantilla que mostrará el formulario de inscripción

    def get(self, request, *args, **kwargs):
        curso_pk = kwargs.get('curso_pk')
        # Filtrar roles sin fecha de finalización (hasta)
        roles_sin_fecha_hasta = Rol.objects.filter(hasta__isnull=True)

        curso = get_object_or_404(Curso, pk=curso_pk)

        inscritosEspera_ids = []
        inscritosEspera_ids = ListaEspera.objects.filter(curso=curso).values_list('rol_id', flat=True)

        incritosEnDictado_dni = []
        dictados = Dictado.objects.all().filter(curso=curso, estado__lt=3).order_by('estado')

        for dictado in dictados:
            # OBTENGO A TODOS MIS ALUMNOS (Alumnos, Afiliado, GrupoFamiliar, Profesores como alumno)
            afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
            familiares_inscritos = Familiar.objects.filter(dictados=dictado)    
            profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
            alumnos_inscritos = Alumno.objects.filter(dictados=dictado)

            # Agregar a la lista
            incritosEnDictado_dni.extend(afiliado_inscritos.values_list('persona__pk', flat=True))
            incritosEnDictado_dni.extend(familiares_inscritos.values_list('persona__pk', flat=True))
            incritosEnDictado_dni.extend(profesores_inscritos.values_list('persona__pk', flat=True))
            incritosEnDictado_dni.extend(alumnos_inscritos.values_list('persona__pk', flat=True))


        # Obtener roles asociados a los inscritos en los dictados
        rolesEnDictado_ids = Rol.objects.filter(persona__pk__in=incritosEnDictado_dni).values_list('id', flat=True)

        print("")
        print("")
        print("")
        print("")
        print("ROLES IDS")
        print(rolesEnDictado_ids)
        # Obtener todos los roles

        # familiares_inscritos_listaEspera = Familiar.objects.filter(lista_espera=dictado)    
        # profesores_inscritos_listaEspera = Profesor.objects.filter(lista_espera=dictado)
        # alumnos_inscritos_listaEspera = Alumno.objects.filter(lista_espera=dictado)
        
        # Calculo la suma total de inscritos
        # total_inscritos = (
        #     afiliado_inscritos.count() +
        #     familiares_inscritos.count() +
        #     profesores_inscritos.count() +
        #     alumnos_inscritos.count()
        # )
        # hay_cupo = total_inscritos < dictado.cupo

        # inscritos_ids = []
        # Agrega los IDs de afiliados, familiares, profesores, alumno
        # inscritos_ids.extend(list(afiliado_inscritos.values_list('persona__pk', flat=True)))
        # inscritos_ids.extend(list(familiares_inscritos.values_list('persona__pk', flat=True)))
        # inscritos_ids.extend(list(profesores_inscritos.values_list('persona__pk', flat=True)))
        # inscritos_ids.extend(list(alumnos_inscritos.values_list('persona__pk', flat=True)))

        # inscritosEspera_ids = []
        # inscritosEspera_ids.extend(list(afiliado_inscritos_listaEspera.values_list('persona__pk', flat=True)))
        # inscritosEspera_ids.extend(list(familiares_inscritos_listaEspera.values_list('persona__pk', flat=True)))
        # inscritosEspera_ids.extend(list(profesores_inscritos_listaEspera.values_list('persona__pk', flat=True)))
        # inscritosEspera_ids.extend(list(alumnos_inscritos_listaEspera.values_list('persona__pk', flat=True)))
        
        # personas = Persona.objects.all()
        
        print("INSCRITOS EN ESPERA: ", inscritosEspera_ids)
        total_en_espera = inscritosEspera_ids.count()
        print("INSCRITOS EN ESPERA: ", total_en_espera)
                
        context = {
            'titulo': 'Incorporación a la lista de espera',
            'curso_pk': curso_pk,
            'roles': roles_sin_fecha_hasta,
            'rolesEnDictado_ids': rolesEnDictado_ids,  # Asegúrate de que esté definida correctamente aquí
            'total_en_espera': total_en_espera,
            'inscritosEspera_ids': inscritosEspera_ids,
        }

        # Convierte inscritosEsperaIds a una cadena JSON para pasarlo a JavaScript
        context['inscritosEsperaIds_json'] = json.dumps(list(inscritosEspera_ids))
        context['inscritosEnDictadoIds_json'] = json.dumps(list(rolesEnDictado_ids))

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

    # OBTENGO A TODOS MIS ALUMNOS (Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
    afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
    familiares_inscritos = Familiar.objects.filter(dictados=dictado)    
    profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
    alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
    # Calculo la suma total de inscritos
    total_inscritos = (
        afiliado_inscritos.count() +
        familiares_inscritos.count() +
        profesores_inscritos.count() +
        alumnos_inscritos.count()
    )
    # OBTENGO A TODOS MIS PERSONAS EN LISTA DE ESPERA(Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
    # afiliado_inscritos_listaEspera = Afiliado.objects.filter(lista_espera=dictado)
    # familiares_inscritos_listaEspera = Familiar.objects.filter(lista_espera=dictado)    
    # profesores_inscritos_listaEspera = Profesor.objects.filter(lista_espera=dictado)
    # alumnos_inscritos_listaEspera = Alumno.objects.filter(lista_espera=dictado)
    
    # Combino todos los objetos en una lista
    # todos_inscritos_listaEspera = list(afiliado_inscritos_listaEspera) + list(familiares_inscritos_listaEspera) + list(profesores_inscritos_listaEspera) + list(alumnos_inscritos_listaEspera)
    hay_cupo = total_inscritos < dictado.cupo
    titulo = 'Lista de espera'

    context = {
        'dictado': dictado,
        # 'todos_inscritos_listaEspera': todos_inscritos_listaEspera,
        'titulo': titulo,
        'hay_cupo': hay_cupo,
        'curso_pk': curso_pk,

    }
    return render(request, 'dictado/dictado_lista_espera.html', context)

# ----------- GESTION DE LISTA DE ESPERA
from django.urls import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect

def gestionListaEspera(request, pk, rol_pk, accion):
    curso = get_object_or_404(Curso, pk=pk)
    
    if accion == 'inscribir_alumno_potencial':
        # Redirige a la vista correspondiente para inscribir al alumno potencial
        url = reverse('cursos:alumno_nuevo_lista_espera', kwargs={'pk': pk})
        return HttpResponseRedirect(url)

    rol = get_object_or_404(Rol, pk=rol_pk)

    if accion == 'incorporar_dictado':
        # Obtén el valor de dictado_id del formulario
        dictado_pk = request.POST.get('dictado_pk')
        dictado = get_object_or_404(Dictado, pk=dictado_pk)
        
        if rol.tipo == 1: 
            persona = get_object_or_404(Afiliado, persona__pk=rol.persona.pk)
        elif rol.tipo == 2: 
            persona = get_object_or_404(Familiar, persona__pk=rol.persona.pk)

        elif rol.tipo == 3:
            persona = get_object_or_404(Alumno, persona__pk=rol.persona.pk)
            persona.es_potencial = False
            persona.save
        elif rol.tipo == 4: 
            persona = get_object_or_404(Profesor, persona__pk=rol.persona.pk)
        elif rol.tipo == 5: 
            # [FALTA: CREAR AL ENCARGADO]
            persona = get_object_or_404(Profesor, persona__pk=rol.persona.pk)
        
        persona.dictados.add(dictado)
        persona.persona.es_alumno = True
        persona.persona.save()                
        persona.save()

        lista_espera_instance = ListaEspera.objects.get(curso=curso, rol=rol)
        lista_espera_instance.delete()
        curso.lista_espera.remove(lista_espera_instance)
        curso.save()

        mensaje_exito(request, f'{MSJ_LISTAESPERA_ELIMINADO_AGREGADO_DICTADO}')
        return redirect('cursos:curso_lista_espera', pk=pk)

    if accion == 'agregar_lista':
        if not ListaEspera.objects.filter(curso=curso, rol=rol).exists():
            # Crea una nueva instancia de ListaEspera y la guarda
            lista_espera_instance = ListaEspera(curso=curso, rol=rol)
            lista_espera_instance.save()
            curso.lista_espera.add(lista_espera_instance)
            curso.save()
            mensaje_exito(request, f'{MSJ_LISTAESPERA_AGREGADO}')
        return redirect('cursos:verificar_persona', curso_pk=pk)

    elif accion == 'quitar_lista':
        # Busca la instancia de ListaEspera relacionada con el Curso y el Rol
        lista_espera_instance = ListaEspera.objects.get(curso=curso, rol=rol)

        # Si tiene rol como alumno
        if lista_espera_instance.rol.tipo == 3: 
            alumno = get_object_or_404(Alumno, persona__pk=lista_espera_instance.rol.persona.pk)
            
            # Cuenta en cuántas listas de espera está mi alumno potencial
            cantidad_listas_espera = ListaEspera.objects.filter(rol=rol).count()

            lista_espera_instance.delete()
            curso.lista_espera.remove(lista_espera_instance)
            curso.save()

            if cantidad_listas_espera == 1 and alumno.es_potencial:
                alumno.delete()
                mensaje_exito(request, f'{MSJ_ALUMNO_POTENCIA_ELIMINADO}')
        else:
            # Elimina la instancia de ListaEspera
            lista_espera_instance.delete()
            # Quítala del campo lista_espera del modelo Curso
            curso.lista_espera.remove(lista_espera_instance)
            curso.save()

        mensaje_exito(request, f'{MSJ_LISTAESPERA_ELIMINADO}')
        return redirect('cursos:curso_lista_espera', pk=pk)
    
    # if accion == 'inscribir':
    #     # persona.lista_espera.remove(dictado)
        
    #     if tipo == 'Profesor':
    #         persona.dictados_inscriptos.add(dictado)
    #     else:
    #         persona.dictados.add(dictado)

    #     persona.persona.es_alumno = True
    #     persona.persona.save()
    #     messages.success(request, f'{ICON_CHECK} {tipo} inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
    
    # elif accion == 'inscribir_alumno_nuevo':
    #     url = reverse('cursos:alumno_nuevo_lista_espera', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})
    #     return HttpResponseRedirect(url)
    
    # elif accion == 'quitar':
    #     # persona.lista_espera.remove(dictado)
    #     messages.success(request, f'{ICON_CHECK} {tipo} sacado de la lista de espera ')
    
    # elif accion == 'agregar_lista':
    #     if tipo == 'Profesor':
    #          # Verificar si existe un Titular con ese Profesor y ese Dictado
    #         titular_existente = Titular.objects.filter(profesor=persona, dictado=dictado).exists()   
    #         if titular_existente:
    #             messages.error(request, f'{ICON_ERROR} Error: El profesor a inscribir es titular del dictado.')
    #             return redirect('cursos:verificar_persona', curso_pk=curso_pk, dictado_pk=dictado_pk)

    #     messages.success(request, f'{ICON_CHECK} {tipo} agregado a la lista de espera. Cierre la ventana y recargue el detalle del dictado')
    #     # persona.lista_espera.add(dictado)
    #     persona.save()
    #     return redirect('cursos:verificar_persona', curso_pk=curso_pk, dictado_pk=dictado_pk)
    
    # persona.save()
    # return redirect('cursos:dictado_lista_espera', curso_pk=curso_pk, dictado_pk=dictado_pk)


# ----------- GESTION DE INSCRIPCION
def gestionInscripcion(request, curso_pk, dictado_pk, persona_pk, tipo, accion):
    dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)

    if tipo == 'Afiliado':
        persona = get_object_or_404(Afiliado, persona__pk=persona_pk)
    elif tipo == 'Familiar':
        persona = get_object_or_404(Familiar, persona__pk=persona_pk)
    elif tipo == 'Profesor':
        persona = get_object_or_404(Profesor, persona__pk=persona_pk)
    elif tipo == 'Alumno':
        persona = get_object_or_404(Alumno, persona__pk=persona_pk)
    elif tipo == 'AlumnoNuevo':
        pass
    else:
        raise Http404("Tipo de persona no válido")

    if accion == 'inscribir':
        if tipo == 'Profesor':
            titular_existente = Titular.objects.filter(profesor=persona, dictado=dictado).exists()      
            if titular_existente:
                messages.error(request, f'{ICON_ERROR} Error: El profesor a inscribir es titular del dictado.')
                return redirect('cursos:verificar_persona', curso_pk=curso_pk, dictado_pk=dictado_pk)
            persona.dictados_inscriptos.add(dictado)
        else:
            persona.dictados.add(dictado)

        persona.persona.es_alumno = True
        persona.persona.save()                
        persona.save()
        messages.success(request, f'{ICON_CHECK} {tipo} inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
        return redirect('cursos:verificar_persona', curso_pk=curso_pk, dictado_pk=dictado_pk)
    
    elif accion == 'inscribir_alumno_nuevo':
        url = reverse('cursos:alumno_nuevo_inscribir', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})
        return HttpResponseRedirect(url)
    
    elif accion == 'desinscribir':

        if tipo == 'Profesor':
            persona.dictados_inscriptos.remove(dictado)
            if not persona.dictados_inscriptos.exists():
                persona.persona.es_alumno = False
                persona.save()
        else:
            persona.dictados.remove(dictado)
            if not persona.dictados.exists():
                persona.persona.es_alumno = False
                persona.save()
        
        persona.persona.save()                
        persona.save()
        messages.success(request, f'{ICON_CHECK} {tipo} ha sido desincrito del curso.')
        return redirect('cursos:dictado_detalle', curso_pk=dictado.curso.pk, dictado_pk=dictado.pk)
    
def finalizarDictado(request, curso_pk, dictado_pk):
    # OBTENEMOS EL DICTADO
    dictado = get_object_or_404(Dictado, pk=dictado_pk)

    # OBTENER TODAS LAS CLASES ASOCIADAS AL DICTADO
    clases_del_dictado = Clase.objects.filter(reserva__horario__dictado=dictado)
    
    # OBTENER LA ÚLTIMA CLASE CON ASISTENCIA TOMADA
    ultima_clase_con_asistencia = Clase.objects.filter(
        reserva__horario__dictado=dictado,
        asistencia_tomada=True
    ).order_by('-reserva__fecha').first()

    print("ULTIMA CLASE")
    print(ultima_clase_con_asistencia)

    #OBTENEMOS LA FECHA QUE SE REALIZO LA CLASE
    fecha = ultima_clase_con_asistencia.reserva.fecha
    #Le asignamos la fecha de fin a mi dictado
    dictado.fecha_fin = fecha
    dictado.estado = 3

    #OBTENEMOS TODAS LAS CLASES QUE NO SE HAN TOMADO ASISTENCIA
    clases_sin_asistencia = clases_del_dictado.filter(asistencia_tomada=False)

    # ELIMINAR LA RESERVA DE LAS CLASES SIN ASISTENCIA
    for clase_sin_asistencia in clases_sin_asistencia:
        reserva = clase_sin_asistencia.reserva
        reserva.delete()

    # BORRAR LAS CLASES SIN ASISTENCIA
    clases_sin_asistencia.delete()

    dictado.save()

    messages.success(request, f'{ICON_CHECK} Dictado finalizado con exito!')
    return redirect('cursos:dictado_detalle', curso_pk=curso_pk, dictado_pk=dictado_pk)


from django.http import FileResponse
from io import BytesIO
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter, landscape

import locale

def generate_pdf(dictado, persona, porcentaje_asistencia):
    buffer = BytesIO()

    # Configurar el tamaño del documento PDF como horizontal
    p = canvas.Canvas(buffer, pagesize=landscape(letter))

    # Configurar el título y el contenido del certificado
    titulo = f"Certificado de Asistencia"

    # Configurar la posición y el estilo del texto en el PDF
    p.setFont("Helvetica-Bold", 46)
    p.drawCentredString(400, 510, titulo)
    
    p.setFont("Helvetica", 40)
    contenido = f"Certificamos que"
    p.drawCentredString(400, 450, contenido)
    
    p.setFont("Helvetica", 35)
    contenido = f"{persona.nombre.upper()} {persona.apellido.upper()}."
    p.drawCentredString(400, 390, contenido)
    
    p.setStrokeColorRGB(0.6, 0.6, 0.6)
    p.line(100, 380, 700 ,380)
    p.setStrokeColorRGB(0, 0, 0)

    p.setFont("Helvetica", 20)
    contenido = f"Participó del curso {dictado.curso.nombre}, organizado por el SEC 2. El"
    p.drawString(100, 340, contenido)
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener la fecha en el formato deseado
    fecha_str = dictado.fecha.strftime("%d de %B del %Y")
    
    contenido = f"mismo se llevó a cabo en la localidad de Trelew del {fecha_str}"
    p.drawString(100, 310, contenido)

    fecha_fin_str = dictado.fecha_fin.strftime("%d de %B del %Y")
    contenido = f"al {fecha_fin_str}. Cumpliendo con un porcentaje de"
    p.drawString(100, 280, contenido)

    contenido = f"asistencia del {porcentaje_asistencia}% "
    p.drawString(100, 250, contenido)
    
    p.setStrokeColorRGB(0.6, 0.6, 0.6)
    p.line(150, 100, 300 ,100)
    p.setStrokeColorRGB(0, 0, 0)
    
    p.setFont("Helvetica", 12)
    contenido = f"Firma y aclaración"
    p.drawString(175, 85, contenido)
    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def generarPDF_Afiliado(request, dictado_pk, persona_pk):
    persona = get_object_or_404(Persona, pk=persona_pk)
    dictado = get_object_or_404(Dictado, pk=dictado_pk)

    # Obtener las clases del dictado
    clases = Clase.objects.filter(reserva__horario__dictado=dictado)

    # Contar las clases a las que asistió el alumno
    clases_asistidas = clases.filter(asistencia__persona=persona)

    # Calcular el porcentaje de asistencia
    porcentaje_asistencia = round((clases_asistidas.count() / clases.count()) * 100)
    print(porcentaje_asistencia)
    # Verificar si el alumno cumple con el 80% de asistencia
    # if porcentaje_asistencia >= 80:
    buffer = generate_pdf(dictado, persona, porcentaje_asistencia)
    return FileResponse(buffer, as_attachment=True, filename="certifiado.pdf")
    # else:
        # Puedes manejar aquí el caso en el que el alumno no cumple con el 80% de asistencia
        # return HttpResponse("El alumno no cumple con el 80% de asistencia requerido.")


from django.db.models import Count, F


def obtenerPorcentajeAsistencia(dictado,profesor):
    
    # ultimo_dia_mes_anterior = obtenerUltimoDiaMesAnterior()
    # primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

    #Por mes actual
    ultimo_dia_mes_actual = timezone.now().replace(day=30, month=4)
    primer_dia_mes_actual = ultimo_dia_mes_actual.replace(day=1)
    clases_dictado = Clase.objects.filter(asistencia_tomada=True, 
                                          reserva__horario__dictado=dictado,
                                          reserva__fecha__range=(primer_dia_mes_actual, ultimo_dia_mes_actual)
                                          )
    




    # Contar el número total de clases en el mes actual
    total_clases_mes_actual = clases_dictado.count()
    # Contar el número de clases donde el profesor estuvo presente
    clases_profesor_presente = clases_dictado.filter(asistencia_profesor=profesor)

    # Contar el número total de clases donde el profesor debería haber estado presente
    total_clases_profesor = clases_dictado.annotate(
        total_asistentes_profesor=Count('asistencia_profesor')
    ).filter(total_asistentes_profesor__gt=0).count()

    # Calcular el porcentaje de asistencia del profesor
    if total_clases_profesor > 0:
        porcentaje_asistencia = (clases_profesor_presente.count() / total_clases_profesor) * 100
    else:
        porcentaje_asistencia = 0
    
    # Tengo que devolver la cantidad de clases, porcentaje de asistencia
    return total_clases_mes_actual, porcentaje_asistencia

from django.http import JsonResponse
from django.utils import timezone

def calcularPrecioPagar(precio_base, porcentaje_asistencia):
    if porcentaje_asistencia == 100:
        return precio_base
    elif porcentaje_asistencia > 0:
        return precio_base * (porcentaje_asistencia / 100)
    else:
        return 0
    
def get_dictados_por_titular(request, titular_pk):
    if request.method == 'GET':
        try:
            data = {'dictados': []}  # Initialize data with 'dictados' key as an empty list
            valor_total = 0

            # Obtener al profesor y sus titulares
            profesor = Profesor.objects.get(pk=titular_pk)
            titulares = Titular.objects.filter(profesor=profesor)


            for titular in titulares:
                dictado = titular.dictado
                precio = dictado.precio_real_profesor
                cantidad_clases, porcentaje_asistencia = obtenerPorcentajeAsistencia(dictado,profesor)
                precio_pagar = calcularPrecioPagar(precio, porcentaje_asistencia)
                data['dictados'].append({
                    'nombre': dictado.curso.nombre,
                    'precio': precio,
                    'estado': dictado.get_estado_display(),
                    'cantidad_clases' : cantidad_clases,
                    'porcentaje_asistencia': porcentaje_asistencia,
                    'precioFinal': precio_pagar,
                })
                valor_total += precio_pagar

            # Agregar el valor total al diccionario
            data['valor_total'] = valor_total

            return JsonResponse(data)

        except Profesor.DoesNotExist:
            return JsonResponse({'error': 'Profesor no encontrado'}, status=404)
        except Titular.DoesNotExist:
            return JsonResponse({'error': 'Titular no encontrado'}, status=404)
