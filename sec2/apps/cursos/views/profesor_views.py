from ..models import Profesor, Titular
from ..forms.profesor_forms import *

from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView

from utils.constants import *
from sec2.utils import ListFilterView

## ------------------ CREATE DE PROFESOR ------------------
class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = FormularioProfesor
    template_name = 'profesor/profesor_form.html'  
    success_url = reverse_lazy('cursos:profesores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ="Alta de Profesor"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Profesor dado de alta con exitoso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)
    
class ProfesorListView(ListFilterView):
    model = Profesor
    paginate_by = 100  
    template_name = 'profesor/profesor_list.html'  
    filter_class = ProfesorFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de profesores"
        return context

# class ProfesorUpdateView(UpdateView):
#     model = Profesor
#     form_class = FormularioProfesorUpdateFrom
#     success_url = reverse_lazy('cursos:profesores')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = "Modificar Profesor"
#         return context
    
#     def form_valid(self, form):
#         messages.add_message(self.request, messages.SUCCESS, 'profesor modificada con éxito')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.add_message(self.request, messages.ERROR, form.errors)
#         return super().form_invalid(form)


# class ProfesorDelDictadoListView(ListFilterView):
#     model = Titular
#     paginate_by = 100
    
#     def get_queryset(self):
#         titular = super().get_queryset().filter(dictado__pk=self.kwargs['pk'])
#         return titular