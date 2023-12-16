from ..models import Curso, Actividad, Titular
from ..forms.curso_forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import DetailView
from sec2.utils import ListFilterView
from django.shortcuts import redirect

##--------------- CREATE DE CURSOS--------------------------------
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:curso_listado')
    title = "Formulario Alta de Curso"  # Agrega un título

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.title  # Agrega el título al contexto
        # Verificar si hay alguna actividad
        tiene_actividad = Actividad.objects.exists()
        context['tiene_actividad'] = tiene_actividad
        return context
    
    def get(self, request, *args, **kwargs):
        tiene_actividad = Actividad.objects.exists()

        if tiene_actividad:
            return super().get(request, *args, **kwargs)
        else:
            messages.warning(
                self.request, 
                '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Completa el siguiente formulario para poder crear un Curso!'
            )
            return redirect('cursos:actividad_crear')

    def form_valid(self, form):
        messages.success(self.request, f'{ICON_CHECK} Alta de curso exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        return super().form_invalid(form)

##--------------- CURSO DETALLE --------------------------------
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Curso: {self.object.nombre}"

        # Obtener todos los dictados asociados al curso
        dictados = self.object.dictado_set.all()

        # Crear una lista para almacenar información de cada dictado, incluyendo el nombre del profesor
        dictados_info = []

        for dictado in dictados:
            # Obtener el titular asociado al dictado
            titular = self.get_titular(dictado)

            # Crear un diccionario con la información del dictado y el nombre del profesor
            dictado_info = {
                'dictado': dictado,
                'nombre_profesor': (
                    f"{titular.profesor.persona.nombre} "
                    f"{titular.profesor.persona.apellido}"
                ) if titular else "Sin titular"
            }

            # Agregar el diccionario a la lista
            dictados_info.append(dictado_info)

        # Agregar la lista de dictados con información al contexto
        context['dictados_info'] = dictados_info

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
    paginate_by = 100
    filter_class = CursoFilterForm
    template_name = 'curso/curso_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Cursos"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CursoFilterForm(self.request.GET)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            actividad = form.cleaned_data.get('actividad')
            periodo_pago = form.cleaned_data.get('periodo_pago')
            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if actividad:
                queryset = queryset.filter(actividad=actividad)
            if periodo_pago:
                queryset = queryset.filter(periodo_pago=periodo_pago)
        return queryset

    def get_success_url(self):
        if self.request.POST['submit'] == "Guardar y Crear Dictado":
            return reverse_lazy('cursos:dictado_crear', args=[self.object.pk])
        return super().get_success_url()

##--------------- CURSO UPDATE --------------------------------
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:cursos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Curso"  # Agrega el título al contexto
        return context
    
    def form_valid(self, form):
        curso = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Curso modificado con éxito')
        return redirect('cursos:curso')

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)
    


