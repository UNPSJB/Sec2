from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Actividad, Curso, Aula
from .forms import ActividadForm, CursoForm, AulaForm
from django.urls import reverse_lazy
from django import forms
from django.db.models import Q, Model
from decimal import Decimal
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML


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

def dict_to_query(filtros_dict):
    filtro = Q()
    for attr, value in filtros_dict.items():
        if not value:
            continue
        if type(value) == str:
            if value.isdigit():
                prev_value = value
                value = int(value)
                filtro &= Q(**{attr: value}) | Q(**
                                                 {f'{attr}__icontains': prev_value})
            else:
                attr = f'{attr}__icontains'
                filtro &= Q(**{attr: value})
        # elif isinstance(value, Model) or isinstance(value, int) or isinstance(value, Decimal):
        elif isinstance(value, (Model, int, Decimal, date)):
            filtro &= Q(**{attr: value})
    return filtro

class FiltrosForm(forms.Form):
    orden = forms.CharField(required=False)

    def filter(self, qs, filters):
        return qs.filter(dict_to_query(filters))  # aplicamos filtros

    def sort(self, qs, ordering):
        for o in ordering.split(','):
            if o != '':
                qs = qs.order_by(o)  # aplicamos ordenamiento
        return qs

    def apply(self, qs):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            ordering = cleaned_data.pop("orden", None)
            if len(cleaned_data) > 0:
                qs = self.filter(qs, cleaned_data)
            if ordering:
                qs = self.sort(qs, ordering)
        return qs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method="GET"
        fields = list(self.fields.keys())
        self.helper.layout = Layout(*fields,
            Submit('submit', 'Filtrar', css_class='button white'),) 

class ListFilterView(ListView):
    filter_class = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filter_class:
            context['filtros'] = self.filter_class(self.request.GET)
            context['query'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.filter_class:
            filtros = self.filter_class(self.request.GET)
            return filtros.apply(qs)
        return qs
    
class ActividadFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(required=False, choices=Actividad.AREAS)

class ActividadListView(ListFilterView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    # success_url = reverse_lazy('cursos:cursos')
    
class CursoListView(ListView):
    model = Curso
    paginate_by = 100  
