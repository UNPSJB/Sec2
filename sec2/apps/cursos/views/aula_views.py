from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from ..models import Aula
from ..forms.aula_forms import *
from django.urls import reverse_lazy
from django.contrib import messages

## ------------  CREATE AND LIST AULA -------------------
class AulaCreateListView(CreateView, ListView):
    model = Aula
    template_name = 'aula/aula_alta_listado.html'  
    form_class = AulaForm
    context_object_name = 'aulas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Gestión de Aula"
        context['form'] = self.get_form()
        context['aulas'] = self.get_queryset()  # Use filtered queryset
        context['filtros'] = AulaFilterForm()
        return context

    def get_success_url(self):
        return reverse_lazy('cursos:gestion_aula')
    
    def form_valid(self, form):
        tipo = form.cleaned_data['tipo']
        numero = form.cleaned_data['numero']

        # Verificar si ya existe un registro con el mismo tipo y número
        if Aula.objects.filter(tipo=tipo, numero=numero).exists():
            messages.warning(self.request, f'{ICON_TRIANGLE} Ya existe un aula con el mismo tipo y número.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        messages.success(self.request, f'{ICON_CHECK} Alta de aula exitosa!')
        return response
    
    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} El nombre ya existe o posee caracteres no deseados.')
        return redirect('cursos:gestion_actividad')
    
    def get(self, request, *args, **kwargs):
        # Asegúrate de que el queryset esté disponible antes de llamar a super().get()
        self.object_list = self.get_queryset()
        return super(CreateView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Aula.objects.all()
        # Obtener los filtros del formulario
        filter_form = AulaFilterForm(self.request.GET)
        if filter_form.is_valid():
            capacidad = filter_form.cleaned_data.get('capacidad')
            tipo = filter_form.cleaned_data.get('tipo')

            # Aplicar filtros según sea necesario
            if capacidad:
                queryset = queryset.filter(capacidad__lte=capacidad)
            if tipo:
                queryset = queryset.filter(tipo=tipo)

        # Ordenar de forma descendente por tipo y luego por número
        queryset = queryset.order_by('-tipo', 'numero')
        return queryset
    
    
#---------------- CREACION DE AULA -----------------
class AulaCreateView(CreateView):   
    success_url = reverse_lazy('cursos:aula_crear')

    
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
class AulaDetailView(DetailView):
    model = Aula
    template_name = "aula/aula_detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Aula'
        return context

#--------------- LISTADO -----------------
class AulaListView(ListView):
    model = Aula
    paginate_by = 100  # Define el número de elementos por página
    filter_class = AulaFilterForm
    template_name = 'aula/aula_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí creas una instancia del formulario y la agregas al contexto
        filter_form = AulaFilterForm(self.request.GET)
        context['filtros'] = filter_form
        context['titulo'] = "Aulas"
        return context
    


## ------------ UPDATE -------------------
class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula/aula_alta.html'
    context_object_name = 'aula'
    success_url = reverse_lazy('cursos:gestion_actividad')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Aula"
        context['filtros'] = AulaFilterForm()
        return context

    def form_valid(self, form):
        aula = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Aula modificado con éxito')
        return redirect('cursos:aula_detalle', pk=aula.pk)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

## ------------ ELIMINAR -------------------
def aula_eliminar(request, pk):
    a = Aula.objects.get(pk=pk)
    a.delete()
    messages.success(request, f'<i class="fa-solid fa-square-check fa-beat-fade"></i>   "{ a }" se ha eliminado con éxito.')
    return redirect('cursos:aula_listado')