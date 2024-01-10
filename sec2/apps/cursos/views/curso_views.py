from ..models import Curso, Actividad, Titular
from ..forms.curso_forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage

##--------------- CREATE DE CURSOS--------------------------------
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_alta_convenio.html'
    success_url = reverse_lazy('cursos:curso_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de Curso"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        tipo_curso = self.request.GET.get('tipo', None)
        kwargs['initial'] = {'tipo_curso': tipo_curso}
        return kwargs
    
    def get(self, request, *args, **kwargs):
        tipo_curso = self.request.GET.get('tipo', None)
        if tipo_curso == 'sec':
            self.template_name = 'curso/curso_alta_sec.html'
        elif tipo_curso == 'convenio':
            self.template_name = 'curso/curso_alta_convenio.html'
        else:
            self.template_name = 'curso/seleccion_tipo_curso.html'

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        tipo_curso = self.request.GET.get('tipo', None)

        # Actualizar el valor de es_convenio en base al tipo de curso
        if tipo_curso == 'convenio':
            form.instance.es_convenio = True
        else:
            form.instance.es_convenio = False

        # Guardar el formulario
        result = super().form_valid(form)

        # Mensaje de éxito
        messages.success(self.request, f'{ICON_CHECK} Alta de curso exitosa!')
        print()
        return result

    def form_invalid(self, form):
        messages.warning(self.request, 'Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

##--------------- CURSO DETALLE --------------------------------
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Curso de {self.object.nombre}"
        context['tituloListado'] = 'Dictados Asociados'

        context['dictados_info_start'] = 1

        # Obtener todos los dictados asociados al curso
        dictados = self.object.dictado_set.all()

        # Crear una lista para almacenar información de cada dictado, incluyendo el nombre del profesor
        dictados_info = []

        for i, dictado in enumerate(dictados, start=context['dictados_info_start']):
            # Obtener el titular asociado al dictado
            titular = self.get_titular(dictado)

            # Crear un diccionario con la información del dictado y el nombre del profesor
            dictado_info = {
                'numero': i,
                'dictado': dictado,
                'nombre_profesor': (
                    f"{titular.profesor.persona.apellido} "
                    f"{titular.profesor.persona.nombre}"
                ) if titular else "Sin titular"
            }

            # Agregar el diccionario a la lista
            dictados_info.append(dictado_info)

        # Paginación
        elementos_por_pagina = 3
        paginator = Paginator(dictados_info, elementos_por_pagina)
        pagina = self.request.GET.get('pagina', 1)

        try:
            dictados_info_paginados = paginator.page(pagina)
        except EmptyPage:
            dictados_info_paginados = paginator.page(paginator.num_pages)

        # Agregar la lista de dictados paginados con información al contexto
        context['dictados_info'] = dictados_info_paginados

        return context
    

    def get_titular(self, dictado):
        try:
            titular = Titular.objects.get(dictado=dictado)
            return titular
        except Titular.DoesNotExist:
            return None

##--------------- CURSO LIST --------------------------------
class CursoListView(ListFilterView):
    model = Curso
    paginate_by = 11
    filter_class = CursoFilterForm
    template_name = 'curso/curso_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí creas una instancia del formulario y la agregas al contexto
        filter_form = CursoFilterForm(self.request.GET)
        context['filtros'] = filter_form
        context['titulo'] = "Cursos"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Obtener los filtros del formulario
        filter_form = CursoFilterForm(self.request.GET)
        if filter_form.is_valid():
            nombre = filter_form.cleaned_data.get('nombre')
            area = filter_form.cleaned_data.get('area')
            duracion = filter_form.cleaned_data.get('duracion') 
            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if area:
                queryset = queryset.filter(area=area)
            if duracion is not None:
                queryset = queryset.filter(duracion=duracion)
        
        queryset = queryset.order_by('nombre')
        return queryset

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Dictado":
            return reverse_lazy('cursos:dictado_crear', args=[self.object.pk])
        return super().get_success_url()

##--------------- CURSO UPDATE --------------------------------
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_alta_sec.html'
    success_url = reverse_lazy('cursos:curso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Curso"
        return context
    
    def form_valid(self, form):
        curso = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Curso modificado con éxito')
        return redirect('cursos:curso_detalle', pk=curso.pk)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

