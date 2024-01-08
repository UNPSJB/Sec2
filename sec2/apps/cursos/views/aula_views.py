from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from ..models import Aula
from ..forms.aula_forms import *
from django.urls import reverse_lazy
from django.contrib import messages

#---------------- CREACION DE AULA -----------------
class AulaCreateView(CreateView):   
    model = Aula
    form_class = AulaForm
    template_name = 'aula/aula_alta.html'  
    success_url = reverse_lazy('cursos:aula_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de aula"
        return context
    
    def form_valid(self, form):
        tipo = form.cleaned_data['tipo']
        numero = form.cleaned_data['numero']

        # Verificar si ya existe un registro con el mismo tipo y número
        if Aula.objects.filter(tipo=tipo, numero=numero).exists():
            messages.warning(self.request, f'{ICON_TRIANGLE} Ya existe un aula con el mismo tipo y número.')
            return self.form_invalid(form)

        messages.success(self.request, f'{ICON_CHECK} Alta de aula exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        form.errors.clear()
        return super().form_invalid(form)
    
## ------------ ACTIVIDAD DETALLE -------------------

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
    success_url = reverse_lazy('cursos:aula_listado')
    
