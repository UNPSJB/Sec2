# from ..models import Alumno
from multiprocessing import context
from pyexpat.errors import messages
import uuid

from django.http import HttpResponse

from apps.cursos.models import Clase

from ..forms.alumno_forms import *
from ..forms.curso_forms import *
from ..forms.dictado_forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sec2.utils import ListFilterView
from django.shortcuts import redirect
from utils.constants import *
from django.contrib import messages

# ---------------- ALUMNO CREATE ----------------
class AlumnoCreateView(CreateView):
    model = Persona
    form_class = AlumnoPersonaForm
    template_name = 'alumno/alumno_form.html'

    def get_success_url(self):
        print("----------1----------")
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return reverse_lazy('cursos:persona_inscribir', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})

    def get_context_data(self, **kwargs):
        print("----------2----------")
        context = super().get_context_data(**kwargs)
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        context['unique_identifier'] = f'alumno_form_{uuid.uuid4().hex}'

        # Print or log the values of curso_pk and dictado_pk for debugging
        print(f"curso_pk: {curso_pk}, dictado_pk: {dictado_pk}")
        
        dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
        context['titulo'] = f'Inscripción para {dictado.curso.nombre}'
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        persona_existente = Persona.objects.filter(dni=dni).first()
        
        if persona_existente:
            messages.error(self.request, f'La persona ya está registrada en el sistema.')
            form = AlumnoPersonaForm(self.request.POST)
            return super().form_invalid(form)
        else:
            # La instancia de Alumno no existe, crear una nueva instancia
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
            )
            persona.save()

            # Crear una nueva instancia de Alumno
            alumno = Alumno(
                persona=persona,
                tipo = Alumno.TIPO
            )
            
            alumno.register
            alumno.save()
            
            
            # Agregar el alumno a los dictados seleccionados en el formulario

            curso_pk = self.kwargs.get('curso_pk')
            dictado_pk = self.kwargs.get('dictado_pk')
    
            dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
            
            dictados_seleccionados = form.cleaned_data.get("dictados", [])

            # Agregar el alumno a los dictados seleccionados
            alumno.dictados.add(dictado)
            messages.success(self.request, f'{ICON_CHECK} Alumno inscrito al curso exitosamente!. Cierre la ventana y recargue el detalle del dictado')
            # Agregar el mensaje de éxito para mostrar en el template
            return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.warning(self.request, f'Corrige los errores en el formulario.')
        return super().form_invalid(form)

# ---------------- ALUMNO CREATE ----------------
class AlumnoListaEsperaCreateView(CreateView):
    model = Persona
    form_class = AlumnoPersonaForm
    template_name = 'alumno/alumno_form.html'

    def get_success_url(self):
        print("----------1----------")
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return reverse_lazy('cursos:persona_inscribir', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})

    def get_context_data(self, **kwargs):
        print("----------2----------")
        context = super().get_context_data(**kwargs)
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        context['unique_identifier'] = f'alumno_form_{uuid.uuid4().hex}'

        # Print or log the values of curso_pk and dictado_pk for debugging
        print(f"curso_pk: {curso_pk}, dictado_pk: {dictado_pk}")
        
        dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
        context['titulo'] = f'Inscripción para {dictado.curso.nombre}'
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        persona_existente = Persona.objects.filter(dni=dni).first()
        
        if persona_existente:
            messages.error(self.request, f'La persona ya está registrada en el sistema.')
            form = AlumnoPersonaForm(self.request.POST)
            return super().form_invalid(form)
        else:
            # La instancia de Alumno no existe, crear una nueva instancia
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
            )
            persona.save()

            # Crear una nueva instancia de Alumno
            alumno = Alumno(
                persona=persona,
                tipo = Alumno.TIPO
            )
            
            alumno.register
            alumno.save()
            
            
            # Agregar el alumno a los dictados seleccionados en el formulario

            curso_pk = self.kwargs.get('curso_pk')
            dictado_pk = self.kwargs.get('dictado_pk')
    
            dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
            
            dictados_seleccionados = form.cleaned_data.get("dictados", [])
        
            # No hay cupo, poner al alumno en lista de espera
            alumno.lista_espera.add(dictado)
            messages.warning(self.request, f' El alumno ha sido puesto en lista de espera.Cierre la ventana y recargue el detalle del dictado.')

            return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.warning(self.request, f'Corrige los errores en el formulario.')
        return super().form_invalid(form)
    
#------------ LISTADO DE ALUMNOS DADO UN DICTADO --------------
from django.views.generic import ListView

class AlumnosEnDictadoList(ListView):
    model = Alumno
    paginate_by = 100
    template_name = 'dictado/dictado_alumnos.html'

    def get_queryset(self):
        # Obtener todos los alumnos sin filtrar por dictado
        queryset = Alumno.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE TODOS LOS ALUMNOS'
        return context

def marcar_asistencia(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)

    # Verificar si la clase actual es la primera clase del dictado
    es_primera_clase = not Clase.objects.filter(
        reserva__horario__dictado=clase.reserva.horario.dictado,
        reserva__fecha__lt=clase.reserva.fecha
    ).exists()

    if not es_primera_clase:
        # La clase no es la primera, entonces verificamos la asistencia de la clase anterior
        clase_anterior = Clase.objects.filter(
            reserva__horario__dictado=clase.reserva.horario.dictado,
            reserva__fecha__lt=clase.reserva.fecha
        ).last()

        if not clase_anterior or not clase_anterior.asistencia_tomada:
            # La asistencia de la clase anterior no se ha tomado, mostrar un mensaje de error
            messages.error(request, f'{ICON_ERROR} La asistencia de la clase anterior no se ha tomado.')
            return redirect('cursos:clase_detalle', curso_pk=clase.reserva.horario.dictado.curso.pk, dictado_pk=clase.reserva.horario.dictado.pk, clase_pk=clase.pk)

    if request.method == 'POST':
        # Obtén la lista de IDs de alumnos que se les marcó la asistencia
        alumnos_asistencia_ids = request.POST.getlist('alumnos_asistencia')

        # Obtén los objetos Alumno correspondientes a los IDs seleccionados
        alumnos_asistencia = Alumno.objects.filter(id__in=alumnos_asistencia_ids)

        # Realiza las acciones necesarias con la lista de alumnos marcados
        for alumno in alumnos_asistencia:
            print(f'Alumno marcado como presente: {alumno.persona.nombre} {alumno.persona.apellido}')

        # Establecer la asistencia de los alumnos en la clase
        clase.asistencia.set(alumnos_asistencia)

        # Actualizar el campo asistencia_tomada a True
        clase.asistencia_tomada = True
        clase.save()

        messages.success(request, f'{ICON_CHECK} Asistencia tomada correctamente.')
        return redirect('cursos:dictado_detalle', curso_pk=clase.reserva.horario.dictado.curso.pk, dictado_pk=clase.reserva.horario.dictado.pk)

    messages.error(request, f'{ICON_ERROR} Ha ocurrido un error inesperado.')
    return redirect('cursos:clase_detalle', curso_pk=clase.reserva.horario.dictado.curso.pk, dictado_pk=clase.reserva.horario.dictado.pk, clase_pk=clase.pk)
