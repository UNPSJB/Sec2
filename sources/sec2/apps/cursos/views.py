from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Actividad, Curso, Aula, Profesor, Dictado, Clase, Alumno, Asistencia_alumno,Asistencia_profesor, Pago_alumno, Titular
from django.contrib import messages
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
from django.urls import reverse_lazy
from django import forms
from django.db.models import Q, Model
from decimal import Decimal
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import ListFilterView


def index(request):
  template = loader.get_template('home_curso.html')
  return HttpResponse(template.render())

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

## ------------ CREACION DE ACTIVIDAD -------------------
class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('cursos:actividad_crear')
    template_name = 'cursos/actividad_alta.html'
    form_title = "Formulario Alta de Actividad"  # Define el título como una variable
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.form_title  # Utiliza la variable form_title en el contexto
        return context

    def form_valid(self, form):
        success_message = "Alta de actividad exitosa!"
        messages.success(self.request, f'<i class="fa-solid fa-square-check fa-beat-fade"></i> {success_message}')
        return redirect('cursos:actividades_listado')
    
    def form_invalid(self, form):
        error_message = "Por favor, corrija los errores a continuación."
        messages.warning(self.request, f'<i class="fa-solid fa-triangle-exclamation fa-flip"></i> {error_message}')
        return super().form_invalid(form)
    
    def post(self, *args, **kwargs):
        self.object = None
        form = ActividadForm(self.request.POST)

        if form.is_valid():
            form.save()
            if 'guardar' in self.request.POST:
                self.form_valid(self,form)
                return redirect('cursos:actividad_listado')
            return redirect('cursos:actividad_listado')
        return self.form_invalid(form=form)

## ------------ LISTADO DE ACTIVIDAD -------------------
class ActividadListView(ListFilterView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Actividades"
        return context

class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('cursos:actividades')

def actividad_eliminar(request, pk):
    a = Actividad.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:actividad_listado') 

#class ActividadDeleteView(DeleteView):
#    model = Actividad
#    success_url = reverse_lazy('cursos:actividades')

class ActividadDetailView(DetailView):
    model = Actividad



class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:cursos')
    
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = 100
    filter_class = CursoFilterForm

    def get_success_url(self):
        print(self.object)
        print(self.request.POST)
        if self.request.POST['submit'] == "Guardar y Crear Dictado":
            return reverse_lazy('cursos:dictado_crear', args=[self.object.pk])
        return super().get_success_url()
    
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:cursos')


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
        print(form.errors)
        print(form.non_field_errors())
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

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
        print(curso)
        context['curso'] = curso
        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curso"] = self.kwargs['pk']
        return context
    
    def get_queryset(self):
        print(self.args, self.kwargs)
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
        print(self.args, self.kwargs)
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
        #print("------------------------", form)
        if form.is_valid():
            
            form.save(curso)
        else: 
            print("--------------ERROR----------------", )
            print(form.errors)
        return redirect(self.success_url)

    def alumno_inscribir(request, pk):
         a = Alumno.objects.get(pk=pk)
         print("Imprimiendo")
         print(request)
         print(pk)  
         return redirect('cursos:ver_inscriptos')
    # def alumno_inscribir(request, pk):
    #     a = Alumno.objects.get(pk=pk)
    #     print("Imprimiendo")
    #     # print(request)
    #     # print(pk)  
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
    print("Estoy aca asistencia!")
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
          print(self.args, self.kwargs)
          titular = super().get_queryset().filter(dictado__pk=self.kwargs['pk'])
          
          return titular

class agregarAlumnoCursoListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnosDelDictadoFilterForm

    def get_queryset(self):
          print(self.args, self.kwargs)
          return super().get_queryset().filter(dictado__pk=self.kwargs['pk'])

def registrarAlumnoADictado(request, pk, apk):
    print("hola")
    alumno = Alumno.objects.get(pk=apk)
    dictado = alumno.agregateDictado(pk)
    return redirect('cursos:alumnos_dictado', dictado.pk)

class CursoDetailView (DeleteView):
    model = Curso
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Curso" 
        context['dictados'] = Curso.obtenerDictados     
        return context
   
    
   