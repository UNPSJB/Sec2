from django.shortcuts import get_object_or_404, redirect
from apps.cursos.forms.actividad_forms import ActividadForm
from apps.cursos.models import Curso
from ..forms.curso_forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from sec2.utils import ListFilterView
from django.urls import reverse_lazy

#--------------- CREATE DE CURSOS--------------------------------
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:curso_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_curso = self.request.GET.get('tipo', None)

        if tipo_curso == 'sec':
            context['titulo'] = "Alta de Curso del SEC"
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
        # Actualizar el valor de es_convenio en base al tipo de curso
        if tipo_curso == 'convenio':
            form.instance.es_convenio = True
        else:
            form.instance.es_convenio = False
        # Guardar el formulario
        result = super().form_valid(form)

        form.instance.descripcion = form.cleaned_data['descripcion'].capitalize()
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
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = self.object  # El objeto de curso obtenido de la vista
        
        context['titulo'] = f"Curso: {self.object.nombre}"
        context['tituloListado'] = 'Dictados Asociados'
        
        # Obtener todos los dictados asociados al curso junto con los horarios
        dictados = curso.dictado_set.prefetch_related('horarios').all()
        context['dictados'] = dictados
        # Verificar si hay dictados asociados
        tiene_dictados = dictados.exists()
        context['tiene_dictados'] = tiene_dictados

        return context

##--------------- CURSO LIST --------------------------------
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = 11
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

##--------------- CURSO ELIMINAR --------------------------------
def curso_eliminar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    try:
        curso.delete()
        messages.success(request, f'{ICON_CHECK} El curso se eliminó correctamente!')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar el aula.')
    return redirect('cursos:curso_listado') 