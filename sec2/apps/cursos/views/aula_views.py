from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from ..models import Aula
from ..forms.aula_forms import *
from django.urls import reverse_lazy

class AulaCreateView(CreateView):   
    model = Aula
    form_class = AulaForm
    template_name = 'aula/aula_form.html'  
    success_url = reverse_lazy('cursos:aulas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de alta de aulas"
        return context
    
class AulaListView(ListView):
    model = Aula
    paginate_by = 100  
    filter_class = AulaFilterForm
    template_name = 'aula/aula_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí creas una instancia del formulario y la agregas al contexto
        filter_form = AulaFilterForm(self.request.GET)
        context['filtros'] = filter_form
        context['titulo'] = "Listado de Aulas"
        return context

class AulaDetailView(DetailView):
    model = Aula

class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('cursos:aulas')
    
