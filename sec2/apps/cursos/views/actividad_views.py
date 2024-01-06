from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from ..models import Actividad
from ..forms.actividad_forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

## ------------ CREACION DE ACTIVIDAD -------------------
class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadCreateForm
    template_name = 'actividad/actividad_alta.html'
    success_url = reverse_lazy('cursos:actividad_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario Alta de Actividad"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Actividad'
        context['tituloListado'] = 'Cursos relacionados'
        
        # Obtener todos los cursos relacionados con la actividad actual
        cursos_relacionados = self.object.cursos.all()
        
        # Puedes agregar más información sobre los cursos según tus necesidades
        cursos_info = [
            {
                'pk' : curso.id,
                'nombre': curso.nombre
            }
            for curso in cursos_relacionados
        ]
        
        # Paginación
        elementos_por_pagina = 3
        paginator = Paginator(cursos_info, elementos_por_pagina)
        pagina = self.request.GET.get('pagina', 1)

        try:
            cursos_info_paginados = paginator.page(pagina)
        except EmptyPage:
            cursos_info_paginados = paginator.page(paginator.num_pages)

        # Agregar la lista de dictados paginados con información al contexto
        context['cursos_info'] = cursos_info_paginados

        return context

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
        form.instance.area = self.get_object().area
        actividad = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Actividad modificado con éxito')
        return redirect('cursos:actividad_detalle', pk=actividad.pk)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

## ------------ LISTADO DE ACTIVIDAD -------------------
class ActividadListView(ListView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm
    template_name = 'actividad/actividad_list.html'

    def get_queryset(self):
        queryset = Actividad.objects.all()
        filtros = ActividadFilterForm(self.request.GET)
        if filtros.is_valid():
            if filtros.cleaned_data['nombre']:
                queryset = queryset.filter(nombre__icontains=filtros.cleaned_data['nombre'])
            if filtros.cleaned_data['area']:
                queryset = queryset.filter(area=filtros.cleaned_data['area'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = ActividadFilterForm(self.request.GET)
        context['titulo'] = "Listado de Actividades"
        return context
