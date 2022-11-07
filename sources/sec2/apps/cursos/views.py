from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Actividad, Curso, Aula
from .forms import ActividadForm, CursoForm, AulaForm
from django.urls import reverse_lazy


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
class ActividadListView(ListView):
    model = Actividad
    paginate_by = 100  


class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    # success_url = reverse_lazy('cursos:cursos')
    
class CursoListView(ListView):
    model = Curso
    paginate_by = 100  
