from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from .models import Actividad, Curso, Aula, Profesor, Dictado, Clase, Alumno, Asistencia_alumno,Asistencia_profesor, Pago_alumno, Titular
from django.urls import reverse_lazy
from sec2.utils import ListFilterView
from utils.constants import *

from .forms import (
    ActividadForm, 
    CursoForm, 
    AulaForm , 
    FormularioProfesor,
    DictadoForm, 
    ActividadFilterForm,CursoFilterForm, 
    DictadoFilterForm,
    ProfesorFilterForm,
    ProfesorForm,
    ClaseForm, 
    ClaseFilterForm, 
    FormularioAlumno,
    FormularioDictado,
    FormularioProfesorUpdateFrom,
    AlumnoFilterForm,
    AlumnosDelDictadoFilterForm,
    FormularioPagoAlumno,
    ProfesorDelDictadoFilterForm
    )

####################### PRINCIPAL #######################
def index(request):
  template = loader.get_template('home_curso.html')
  return HttpResponse(template.render())

####################### SECCION DE ACTIVIDAD #######################
## ------------ CREACION DE ACTIVIDAD -------------------
class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/actividad_alta.html'
    success_url = reverse_lazy('cursos:actividad_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ="Formulario Alta de Actividad"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de actividad exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

## ------------ ACTIVIDAD DETALLE -------------------
class ActividadDetailView(DetailView):
    model = Actividad
    template_name = 'actividad/actividad_detalle.html'

## ------------ ACTIVIDAD UPDATE -------------------
class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/actividad_alta.html'
    success_url = reverse_lazy('cursos:actividades')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Actividad"
        return context

    def form_valid(self, form):
        actividad = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Actividad modificado con éxito')
        return redirect('cursos:actividad_listado')

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

## ------------ ACTIVIDAD DELETE -------------------
def actividad_eliminar(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    try:
        actividad.delete()
        messages.success(request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> La actividad se eliminó correctamente.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar la actividad.')
    return redirect('cursos:actividad_listado')

## ------------ LISTADO DE ACTIVIDAD -------------------
class ActividadListView(ListFilterView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm
    template_name = 'actividad/actividad_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Actividades"
        return context

####################### SECCION DE CURSOS #######################
##--------------- CREATE DE CURSOS--------------------------------
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:curso_listado')
    title = "Formulario Alta de Curso"  # Agrega un título

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de curso exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

##--------------- CURSO LIST --------------------------------
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = 100
    filter_class = CursoFilterForm
    template_name = 'curso/curso_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Cursos"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CursoFilterForm(self.request.GET)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            actividad = form.cleaned_data.get('actividad')
            periodo_pago = form.cleaned_data.get('periodo_pago')
            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if actividad:
                queryset = queryset.filter(actividad=actividad)
            if periodo_pago:
                queryset = queryset.filter(periodo_pago=periodo_pago)
        return queryset

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Dictado":
            return reverse_lazy('cursos:dictado_crear', args=[self.object.pk])
        return super().get_success_url()

##--------------- CURSO UPDATE --------------------------------
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:cursos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Curso"  # Agrega el título al contexto
        return context
    
    def form_valid(self, form):
        curso = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Curso modificado con éxito')
        return redirect('cursos:curso')

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

class AulaListView(ListView):
    model = Aula
    paginate_by = 100

class AulaCreateView(CreateView):   
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('cursos:aulas')
    
class AulaDetailView(DetailView):
    model = Aula

class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('cursos:aulas')
    
def aula_eliminar(request, pk):
    a = Aula.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:aulas') 



def curso_eliminar(request, pk):
    a = Curso.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:cursos')

class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = FormularioProfesor
    success_url = reverse_lazy('cursos:profesores')
    
class ProfesorListView(ListFilterView):
    model = Profesor
    # paginate_by = 100  
    filter_class = ProfesorFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de profesores"
        return context


class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = FormularioProfesorUpdateFrom
    success_url = reverse_lazy('cursos:profesores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Profesor"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'profesor modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

##--------------- DICTADO CREATE --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = FormularioDictado
    success_url = reverse_lazy('cursos:cursos')

    def get_initial(self,*args, **kwargs):
        curso= Curso.objects.get(pk=self.kwargs.get("pk"))
        return {'curso':curso}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id = self.kwargs.get('pk'))
        context['curso'] = curso
        return context

##--------------- DICTADO DETALLE --------------------------------
class DictadoDetailView (DeleteView):
    model = Dictado
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Dictado" 
        return context

class DictadoListView(ListFilterView):
    model = Dictado
    paginate_by = 100
    filter_class = DictadoFilterForm
    template_name = 'dictado/dictado_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Dictados del curso"
        context["curso"] = self.kwargs['pk']
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(curso__pk=self.kwargs['pk'])
    
class AlumnosListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnoFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curso"] = self.kwargs['pk']
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(curso__pk=self.kwargs['pk'])

 

class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
   
    success_url = reverse_lazy('cursos:cursos')
    
    def post(self, *args, **kwargs):
        form = ClaseForm(self.request.POST)
        dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
        if form.is_valid():
            form.save(dictado)
        return redirect(self.success_url)

class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm



class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = FormularioAlumno
    success_url = reverse_lazy('cursos:cursos')

    def get_initial(self,*args, **kwargs):
        curso= Curso.objects.get(pk=self.kwargs.get("pk"))
        return {'curso':curso}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id = self.kwargs.get('pk'))
        context['curso'] = curso
        return context
    
    def post(self, *args, **kwargs):
        form = self.get_form()
        curso = Curso.objects.get(pk=self.kwargs.get("pk"))
        if form.is_valid():
            
            form.save(curso)
        else: 
            return redirect(self.success_url)

    def alumno_inscribir(request, pk):
         a = Alumno.objects.get(pk=pk)
         return redirect('cursos:ver_inscriptos')
    # def alumno_inscribir(request, pk):
    #     a = Alumno.objects.get(pk=pk)
    #     return redirect('cursos:ver_inscriptos')

    # def get_initial(self,*args, **kwargs):
    #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
    #     return {'dictado':dictado}
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
    #     context['dictado'] = dictado
    #     return context
    
    # def post(self, *args, **kwargs):
    #     form = self.get_form()
    #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
    #     return redirect(self.success_url)

   
# class AlumnosListView(ListView):
#     model = Alumno
#     paginate_by = 100
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['dictado'] = Alumno.objects.get(id = self.kwargs.get('pk'))
#         return context

class AlumnosDelDictadoListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnosDelDictadoFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
        context['dictado'] = dictado
        return context

    def get_queryset(self):        
        return super().get_queryset().filter(curso_id=self.kwargs['pk'])
    
def registrarAsistenciaAlumno(request, pk, apk):
    asistencia_alumno = Asistencia_alumno(dictado_id=pk, alumno_id=apk)
    asistencia_alumno.save()
    dictado = Dictado.objects.get(pk=pk)
    curso = Curso.objects.get(pk=dictado.curso.pk)
    return redirect('cursos:alumnos_dictado',curso.pk)   

def registrarAsistenciaProfesor(request, pk, ppk):
    titular = Titular.objects.filter(titular_dictado_pk=pk)
    asistencia_profesor = Asistencia_profesor(titular)
    asistencia_profesor.save()

class PagoAlumnoCreateView(CreateView):
    model = Pago_alumno
    form_class = FormularioPagoAlumno
    success_url = reverse_lazy('cursos:cursos')
 
class ProfesorDelDictadoListView(ListFilterView):
    model = Titular
    paginate_by = 100
    filter_class = ProfesorDelDictadoFilterForm
    
    def get_queryset(self):
          titular = super().get_queryset().filter(dictado__pk=self.kwargs['pk'])
          
          return titular

class agregarAlumnoCursoListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnosDelDictadoFilterForm

    def get_queryset(self):
          return super().get_queryset().filter(dictado__pk=self.kwargs['pk'])

def registrarAlumnoADictado(request, pk, apk):
    alumno = Alumno.objects.get(pk=apk)
    dictado = alumno.agregateDictado(pk)
    return redirect('cursos:alumnos_dictado', dictado.pk)

class CursoDetailView (DeleteView):
    model = Curso
    template_name = 'curso/curso_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle de Curso" 
        context['dictados'] = Curso.obtenerDictados     
        return context