# from ..models import Alumno
from pyexpat.errors import messages

from ..forms.alumno_forms import *
from ..forms.curso_forms import *
from ..forms.dictado_forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sec2.utils import ListFilterView
from django.shortcuts import redirect
from utils.constants import *
from django.contrib import messages

# ---------------- ALUMNO CREATE ----------------
class AlumnoCreateView(CreateView):
    model = Persona
    form_class = AlumnoPersonaForm
    template_name = 'alumno/alumno_form.html'

    def get_success_url(self):
        print("-----------1-----------")
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        return reverse_lazy('cursos:dictado_detalle', kwargs={'curso_pk': curso_pk, 'dictado_pk': dictado_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_pk = self.kwargs.get('curso_pk')
        dictado_pk = self.kwargs.get('dictado_pk')
        
        # Print or log the values of curso_pk and dictado_pk for debugging
        print(f"curso_pk: {curso_pk}, dictado_pk: {dictado_pk}")
        
        dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
        context['titulo'] = f'Formulario de Alumno - Dictado: {dictado} - Curso: {dictado.curso.nombre}'
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        persona_existente = Persona.objects.filter(dni=dni).first()
        
        if persona_existente:
            messages.error(self.request, f'La persona ya está registrada en el sistema.')
            form = AlumnoPersonaForm(self.request.POST)
            return super().form_invalid(form)
        else:
            # La instancia de Alumno no existe, crear una nueva instancia
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
            )
            persona.save()

            # Crear una nueva instancia de Alumno
            alumno = Alumno(
                persona=persona,
                tipo = Alumno.TIPO
            )
            
            alumno.register
            alumno.save()
            
            
            # Agregar el alumno a los dictados seleccionados en el formulario

            curso_pk = self.kwargs.get('curso_pk')
            dictado_pk = self.kwargs.get('dictado_pk')
    
            dictado = get_object_or_404(Dictado, curso__pk=curso_pk, pk=dictado_pk)
            
            dictados_seleccionados = form.cleaned_data.get("dictados", [])

            # Agregar el alumno a los dictados seleccionados
            alumno.dictados.add(dictado)
            messages.success(self.request, f'Alumno inscrito al curso exitosamente!')

            return super().form_valid(form)
        
    def form_invalid(self, form):
        print("-----------6-----------")
        messages.warning(self.request, f'Corrige los errores en el formulario.')
        return super().form_invalid(form)

#------------ LISTADO DE ALUMNOS DADO UN DICTADO --------------
from django.views.generic import ListView

class AlumnosEnDictadoList(ListView):
    model = Alumno
    paginate_by = 100
    template_name = 'dictado/dictado_alumnos.html'

    def get_queryset(self):
        # Obtener todos los alumnos sin filtrar por dictado
        queryset = Alumno.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE TODOS LOS ALUMNOS'
        return context


#     model = Alumno
#     paginate_by = 100
#     # filter_class = AlumnosDelDictadoFilterForm
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
#         context['dictado'] = dictado
#         return context

#     def get_queryset(self):        
#         return super().get_queryset().filter(curso_id=self.kwargs['pk'])
    
# class agregarAlumnoCursoListView(ListFilterView):
#     model = Alumno
#     paginate_by = 100
#     # filter_class = AlumnosDelDictadoFilterForm

#     def get_queryset(self):
#         return super().get_queryset().filter(dictado__pk=self.kwargs['pk'])