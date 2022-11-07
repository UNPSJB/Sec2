from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Actividad, Curso
from .forms import ActividadForm, CursoForm
from django.urls import reverse_lazy

# Create your views here.
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