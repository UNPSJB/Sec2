from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Actividad, Curso, Aula, Profesor,Dictado
from .forms import ActividadForm, CursoForm, AulaForm , FormularioProfesor,DictadoForm, ActividadFilterForm,CursoFilterForm,DictadoFilterForm
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

class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('cursos:actividades')

class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('cursos:actividades')

def actividad_eliminar(request, pk):
    a = Actividad.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:actividades') 

#class ActividadDeleteView(DeleteView):
#    model = Actividad
#    success_url = reverse_lazy('cursos:actividades')

class ActividadDetailView(DetailView):
    model = Actividad


     


class ActividadListView(ListFilterView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('cursos:cursos')
    
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = 100
    filter_class = CursoFilterForm


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
    success_url = reverse_lazy('cursos:Profesor_crear')

class DictadoCreateView(CreateView):
    model = Dictado
    form_class = DictadoForm

class DictadoListView(ListFilterView):
    model = Dictado
    paginate_by = 100
    filter_class = DictadoFilterForm