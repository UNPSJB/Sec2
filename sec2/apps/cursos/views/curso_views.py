from django.shortcuts import get_object_or_404, redirect
from apps.cursos.forms.actividad_forms import ActividadForm
from apps.cursos.models import Curso, Dictado
from apps.personas.models import Persona, Rol
from utils.funciones import mensaje_error, mensaje_exito
from ..forms.curso_forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from sec2.utils import ListFilterView
from django.urls import reverse_lazy
from django.shortcuts import render

#--------------- CREATE DE CURSOS--------------------------------
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:curso_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_curso = self.request.GET.get('tipo', None)
        context['actividades'] = Actividad.objects.all().order_by('nombre')
        if tipo_curso == 'sec':
            context['titulo'] = "Alta de Curso del SEC 2"
        elif tipo_curso == 'convenio':
            context['titulo'] = "Alta de Convenio"
        elif tipo_curso == 'actividad':
            context['titulo'] = "Alta de Gimnasia"
        else:
            context['titulo'] = "Tipo de Curso"  # Default title
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        tipo_curso = self.request.GET.get('tipo', None)
        kwargs['initial'] = {'tipo_curso': tipo_curso}
        return kwargs
    
    def get(self, request, *args, **kwargs):
        tipo_curso = self.request.GET.get('tipo', None)
        if tipo_curso == 'sec':
            self.template_name = 'curso/curso_alta_sec.html'
        elif tipo_curso == 'convenio':
            self.template_name = 'curso/curso_alta_convenio.html'
        elif tipo_curso == 'actividad':
            self.template_name = 'curso/curso_alta_gimnasio.html'
        else:
            self.template_name = 'curso/seleccion_tipo_curso.html'

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        tipo_curso = self.request.GET.get('tipo', None)
    # Obtener el ID de la actividad seleccionada en el formulario
        actividad_id = self.request.POST.get('enc_cliente')        
        print("ACTIVIDAAAAD----")
        print(actividad_id)
        actividad = get_object_or_404(Actividad, pk=actividad_id)

        # Actualizar el valor de es_convenio en base al tipo de curso
        if tipo_curso == 'convenio':
            form.instance.es_convenio = True
        else:
            form.instance.es_convenio = False
        # Guardar el formulario
        # form.instance.actividad = actividad
        result = super().form_valid(form)
        
        form.instance.actividad = actividad
        form.instance.descripcion = form.cleaned_data['descripcion'].capitalize()
        # form.instance.descripcion = form.cleaned_data['descripcion'].capitalize()
        form.instance.nombre = form.cleaned_data['nombre'].title()
        form.save()
        messages.success(self.request, f'{ICON_CHECK} Alta de curso exitosa!')
        return result

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Por favor, corrija los errores a continuación.')
        # Imprimir los errores en la consola
        print("Errores del formulario:", form.errors)

        # Cambiar el template según el tipo de curso
        tipo_curso = self.request.GET.get('tipo', None)
        if tipo_curso == 'sec':
            self.template_name = 'curso/curso_alta_sec.html'
        elif tipo_curso == 'convenio':
            self.template_name = 'curso/curso_alta_convenio.html'
        elif tipo_curso == 'actividad':
            self.template_name = 'curso/curso_alta_gimnasio.html'
        else:
            self.template_name = 'curso/seleccion_tipo_curso.html'

        return super().form_invalid(form)
    
#--------------- CURSO DETALLE --------------------------------
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detalle.html'
    paginate_by = MAXIMO_PAGINATOR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = self.object  # El objeto de curso obtenido de la vista

        context['titulo'] = f"{self.object.nombre}"
        context['tituloListado'] = 'Dictados Asociados'

        # Obtener todos los dictados asociados al curso junto con los horarios
        dictados = curso.dictado_set.prefetch_related('horarios').all()
        
        context['tiene_dictados'] = dictados.exists()

        # Configurar la paginación
        paginator = Paginator(dictados, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            dictados = paginator.page(page)
        except PageNotAnInteger:
            dictados = paginator.page(1)
        except EmptyPage:
            dictados = paginator.page(paginator.num_pages)

        context['dictados'] = dictados

        return context

##--------------- CURSO LIST --------------------------------
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = MAXIMO_PAGINATOR
    filter_class = CursoFilterForm
    template_name = 'curso/curso_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí creas una instancia del formulario y la agregas al contexto
        filter_form = CursoFilterForm(self.request.GET)
        context['filtros'] = filter_form
        context['titulo'] = "Cursos"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Obtener los filtros del formulario
        filter_form = CursoFilterForm(self.request.GET)
        if filter_form.is_valid():
            area = filter_form.cleaned_data.get('area')
            nombre = filter_form.cleaned_data.get('nombre')
            duracion = filter_form.cleaned_data.get('duracion')
            actividad = filter_form.cleaned_data.get('actividades')
            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if area:
                queryset = queryset.filter(area=area)
            if duracion is not None:
                queryset = queryset.filter(duracion=duracion)
            if actividad:
                queryset = queryset.filter(actividad=actividad)
        queryset = queryset.order_by('area', 'nombre')
        return queryset

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Dictado":
            return reverse_lazy('cursos:dictado_crear', args=[self.object.pk])
        return super().get_success_url()

##--------------- CURSO UPDATE --------------------------------
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:curso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_curso = self.get_object().get_tipo_curso()  # Obtén el tipo de curso
        context['tipo_curso'] = tipo_curso
        
        if tipo_curso == 'sec':
            context['titulo'] = "Modificar Curso del Sec"
        elif tipo_curso == 'convenio':
            context['titulo'] = "Modificar Convenio"
        elif tipo_curso == 'actividad':
            context['titulo'] = "Modificar Curso3"
        else:
            context['titulo'] = "Modificar Curso5"
        
        context['actividades'] = Actividad.objects.all().order_by('nombre')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        tipo_curso = self.get_object().get_tipo_curso()  # Obtén el tipo de curso
        kwargs['initial'] = {'tipo_curso': tipo_curso}
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        requiere_certificado_medico = self.object.requiere_certificado_medico
        
        if requiere_certificado_medico:
            self.template_name = 'curso/curso_alta_gimnasio.html'
        else:
            es_convenio = self.object.es_convenio
            if es_convenio:
                self.template_name = 'curso/curso_alta_convenio.html'
            else:
                self.template_name = 'curso/curso_alta_sec.html'
        return super().get(request, *args, **kwargs)
        
    def form_valid(self, form):
        curso = form.save()
        messages.success(self.request, f'{ICON_CHECK} Curso modificado con éxito')
        return redirect('cursos:curso_detalle', pk=curso.pk)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Por favor, corrija los errores a continuación.')
        # Imprimir los errores en la consola
        print("Errores del formulario:", form.errors)
        tipo_curso = self.get_object().get_tipo_curso()  # Obtén el tipo de curso
        if tipo_curso == 'sec':
            self.template_name = 'curso/curso_alta_sec.html'
        elif tipo_curso == 'convenio':
            self.template_name = 'curso/curso_alta_convenio.html'
        elif tipo_curso == 'actividad':
            self.template_name = 'curso/curso_alta_gimnasio.html'
        else:
            self.template_name = 'curso/seleccion_tipo_curso.html'

        return super().form_invalid(form)

def cursoListaEspera(request, pk):
    # Obtener el objeto Dictado
    curso = Curso.objects.get(id=pk)
    dictados = Dictado.objects.all().filter(curso=curso, estado__lt=3).order_by('estado')

    titulo = f'Inscritos en espera para {curso.nombre}'

    # Obtener la lista de espera ordenada por tipo y fecha de inscripción
    lista_espera = ListaEspera.objects.filter(curso=curso).order_by('rol__tipo', 'fechaInscripcion')

    # OBTENGO A TODOS MIS ALUMNOS (Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
    # afiliado_inscritos = Afiliado.objects.filter(dictados=dictado)
    # familiares_inscritos = Familiar.objects.filter(dictados=dictado)    
    # profesores_inscritos = Profesor.objects.filter(dictados_inscriptos=dictado)
    # alumnos_inscritos = Alumno.objects.filter(dictados=dictado)
    # Calculo la suma total de inscritos
    # total_inscritos = (
    #     afiliado_inscritos.count() +
    #     familiares_inscritos.count() +
    #     profesores_inscritos.count() +
    #     alumnos_inscritos.count()
    # )
    # OBTENGO A TODOS MIS PERSONAS EN LISTA DE ESPERA(Alumnos, Afiliado, GrupoFamiliar, Profeosres como alumno)
    # afiliado_inscritos_listaEspera = Afiliado.objects.filter(lista_espera=dictado)
    # familiares_inscritos_listaEspera = Familiar.objects.filter(lista_espera=dictado)    
    # profesores_inscritos_listaEspera = Profesor.objects.filter(lista_espera=dictado)
    # alumnos_inscritos_listaEspera = Alumno.objects.filter(lista_espera=dictado)
    
    # Combino todos los objetos en una lista
    # todos_inscritos_listaEspera = list(afiliado_inscritos_listaEspera) + list(familiares_inscritos_listaEspera) + list(profesores_inscritos_listaEspera) + list(alumnos_inscritos_listaEspera)
    # hay_cupo = total_inscritos < dictado.cupo

    context = {
        'curso': curso,
        'dictados': dictados,
        # 'todos_inscritos_listaEspera': todos_inscritos_listaEspera,
        'titulo': titulo,
        'lista_espera': lista_espera,

        # 'hay_cupo': hay_cupo,
        'curso_pk': pk,

    }
    return render(request, 'curso/curso_lista_espera.html', context)


from django.utils import timezone

##--------------- CURSO ELIMINAR --------------------------------
def curso_eliminar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    try:
        if dictadosFinalizados(curso):
            curso.fechaBaja = timezone.now()
            curso.save()
            mensaje_exito(request, f'El curso ha sido deshabilitado con exito')
        else:
            mensaje_error(request, f'No se puede eliminar el curso porque tiene dictados que no han finalizado')

    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar el aula.')
    return redirect('cursos:curso_listado') 


def dictadosFinalizados(curso):
    dictados = Dictado.objects.all().filter(curso=curso)
    print(dictados)
    for dictado in dictados:
        print(dictado.estado)
        if not dictado.estado == 3:
            return False
    
    return True