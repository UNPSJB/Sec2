from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from .models import Actividad, Curso, Aula, Profesor, Dictado, Clase, Alumno, Asistencia_alumno,Asistencia_profesor, Pago_alumno, Titular
from django.urls import reverse_lazy
from sec2.utils import ListFilterView
from utils.constants import *
from django.shortcuts import render
from django.urls import reverse

from .forms import (
    ActividadForm, 
    CursoForm, 
    AulaForm , 
    FormularioProfesor,
    DictadoForm, 
    AulaFilterForm,
    ActividadFilterForm,CursoFilterForm, 
    DictadoFilterForm,
    ProfesorFilterForm,
    ProfesorForm,
    ClaseForm, 
    ClaseFilterForm, 
    FormularioAlumno,
    FormularioDictado,
    FormularioProfesorUpdateFrom,
    AlumnoFilterForm,
    AlumnosDelDictadoFilterForm,
    FormularioPagoAlumno,
    ProfesorDelDictadoFilterForm
    )

####################### PRINCIPAL #######################
def index(request):
  template = loader.get_template('home_curso.html')
  return HttpResponse(template.render())

####################### SECCION DE ACTIVIDAD #######################
## ------------ CREACION DE ACTIVIDAD -------------------
class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/actividad_alta.html'
    success_url = reverse_lazy('cursos:actividad_listado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ="Formulario Alta de Actividad"
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
        actividad = form.save()
        messages.success(self.request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> Actividad modificado con éxito')
        return redirect('cursos:actividad_listado')

    def form_invalid(self, form):
        messages.warning(self.request, '<i class="fa-solid fa-triangle-exclamation fa-flip"></i> Por favor, corrija los errores a continuación.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)

## ------------ ACTIVIDAD DELETE -------------------
def actividad_eliminar(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    try:
        actividad.delete()
        messages.success(request, '<i class="fa-solid fa-square-check fa-beat-fade"></i> La actividad se eliminó correctamente.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al intentar eliminar la actividad.')
    return redirect('cursos:actividad_listado')

## ------------ LISTADO DE ACTIVIDAD -------------------
class ActividadListView(ListFilterView):
    model = Actividad
    paginate_by = 100  
    filter_class = ActividadFilterForm
    template_name = 'actividad/actividad_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Actividades"
        return context

####################### SECCION DE CURSOS #######################
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
        # Verificar si hay alguna actividad antes de renderizar el formulario
        tiene_actividad = Actividad.objects.exists()
        
        if tiene_actividad:
            # return render(request, 'curso/curso_form.html', {'titulo': 'te falta calle'})
            return super().get(request, *args, **kwargs)
        else:
            # Renderizar un mensaje indicando que falta crear una actividad
            return render(request, 'curso/falta_actividad.html', {'titulo': 'Te falta menos calle'})

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


####################### SECCION DE AULA #######################
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
    
def aula_eliminar(request, pk):
    a = Aula.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:aulas') 



def curso_eliminar(request, pk):
    a = Curso.objects.get(pk=pk)
    a.delete()
    return redirect('cursos:cursos')

####################### SECCION DE PROFESOR #######################
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

class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = FormularioProfesorUpdateFrom
    success_url = reverse_lazy('cursos:profesores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Profesor"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'profesor modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


####################### SECCION DE DICTADO #######################
##--------------- CREACION DE DICTADO --------------------------------
class DictadoCreateView(CreateView):
    model = Dictado
    form_class = FormularioDictado
    template_name = 'dictado/dictado_form.html'

    def get_initial(self,*args, **kwargs):
        curso= Curso.objects.get(pk=self.kwargs.get("pk"))
        return {'curso':curso}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id = self.kwargs.get('pk'))
        context['curso'] = curso
        context['titulo'] = f"Alta de dictado para el curso {curso.nombre}"
        tiene_profesor = Profesor.objects.exists()
        context['tiene_profesor'] = tiene_profesor
        return context

    def get(self, request, *args, **kwargs):
        # Verificar si hay alguna actividad antes de renderizar el formulario
        if Profesor.objects.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'dictado/falta_profesor.html', {'titulo': 'Te falta menos calle'})

    def get_success_url(self):
        # Obtiene el pk del curso desde los kwargs de la vista
        pk_curso = self.kwargs.get('pk', None)
        # Construye la URL inversa con el pk del curso
        return reverse('cursos:dictados_listado', kwargs={'pk': pk_curso})

##--------------- DICTADO DETALLE --------------------------------
class DictadoDetailView(DetailView):
    model = Dictado
    template_name = 'dictado/dictado_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el nombre del profesor asociado al dictado
        titular = self.get_titular(context['object'])
        context['nombre_profesor'] = (
            f"{titular.profesor.persona.nombre}, "
            f"{titular.profesor.persona.apellido}"
        ) if titular else "Sin titular"

        # Obtener todas las clases asociadas al dictado
        clases = Clase.objects.filter(dictado=context['object'])
        context['clases'] = clases

        context['titulo'] = "Dictado"
        return context

    def get_titular(self, dictado):
        try:
            titular = dictado.titular_set.get()  # Acceder al titular asociado al dictado
            return titular
        except Titular.DoesNotExist:
            return None

##--------------- DICTADO LIST VIEW --------------------------------
class DictadoListView(ListView):
    model = Dictado
    paginate_by = 100
    filter_class = DictadoFilterForm
    template_name = 'dictado/dictado_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id=self.kwargs.get('pk'))
        context['titulo'] = f"Listado de dictado para {curso.nombre}"
        context["curso"] = self.kwargs['pk']
        return context

    def get_queryset(self):
        dictados = super().get_queryset().filter(curso__pk=self.kwargs['pk'])

        # Agregar información del titular para cada dictado
        for dictado in dictados:
            titular = self.get_titular(dictado)
            dictado.titular = titular
        return dictados

    def get_titular(self, dictado):
        try:
            titular = Titular.objects.get(dictado=dictado)
            return titular.profesor
        except Titular.DoesNotExist:
            return None


####################### SECCION DE CLASE #######################
##--------------- CREACION DE CLASE --------------------------------
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clase/clase_form.html'
    success_url = None  # Asigna un valor predeterminado a success_url

    def get_initial(self,*args, **kwargs):
        dictado= Dictado.objects.get(pk=self.kwargs.get("pk"))
        return {'dictado':dictado}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
        context['dictado'] = dictado
        context['titulo'] = f"Alta de clase para el dictado {dictado.cantidad_clase}"
        tiene_aula = Aula.objects.exists()
        context['tiene_aula'] = tiene_aula
        return context

    def get(self, request, *args, **kwargs):
        # Verificar si hay alguna actividad antes de renderizar el formulario
        if Aula.objects.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'clase/falta_aula.html', {'titulo': 'Te falta menos calle'})

    def post(self, request, *args, **kwargs):
        form = ClaseForm(request.POST)
        dictado_id = kwargs.get("pk")
        dictado = Dictado.objects.get(pk=dictado_id)

        if form.is_valid():
            form.save(dictado)

            # Redirige a la vista DictadoDetailView con el pk del dictado
            return redirect('cursos:dictado', pk=dictado_id)
        else:
            context = {'form': form, 'dictado_id': dictado_id, 'titulo': f"Alta de clase para el dictado {dictado.cantidad_clase}"}
            return render(request, self.template_name, context)


    def get_success_url(self):
        # La redirección se maneja en el método post, por lo que este método puede retornar cualquier cosa (por ejemplo, None)
        return None
    
    def form_valid(self, form):
        dictado_id = self.kwargs.get('pk')
        dictado = Dictado.objects.get(pk=dictado_id)
        form.save(dictado)
        return super().form_valid(form)


class AlumnosListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnoFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curso"] = self.kwargs['pk']
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(curso__pk=self.kwargs['pk'])



####################### SECCION DE CLASE #######################






class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm



class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = FormularioAlumno
    success_url = reverse_lazy('cursos:cursos')

    def get_initial(self,*args, **kwargs):
        curso= Curso.objects.get(pk=self.kwargs.get("pk"))
        return {'curso':curso}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(id = self.kwargs.get('pk'))
        context['curso'] = curso
        return context
    
    def post(self, *args, **kwargs):
        form = self.get_form()
        curso = Curso.objects.get(pk=self.kwargs.get("pk"))
        if form.is_valid():
            
            form.save(curso)
        else: 
            return redirect(self.success_url)

    def alumno_inscribir(request, pk):
         a = Alumno.objects.get(pk=pk)
         return redirect('cursos:ver_inscriptos')
    # def alumno_inscribir(request, pk):
    #     a = Alumno.objects.get(pk=pk)
    #     return redirect('cursos:ver_inscriptos')

    # def get_initial(self,*args, **kwargs):
    #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
    #     return {'dictado':dictado}
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
    #     context['dictado'] = dictado
    #     return context
    
    # def post(self, *args, **kwargs):
    #     form = self.get_form()
    #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
    #     return redirect(self.success_url)

   
# class AlumnosListView(ListView):
#     model = Alumno
#     paginate_by = 100
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['dictado'] = Alumno.objects.get(id = self.kwargs.get('pk'))
#         return context

class AlumnosDelDictadoListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnosDelDictadoFilterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
        context['dictado'] = dictado
        return context

    def get_queryset(self):        
        return super().get_queryset().filter(curso_id=self.kwargs['pk'])
    
def registrarAsistenciaAlumno(request, pk, apk):
    asistencia_alumno = Asistencia_alumno(dictado_id=pk, alumno_id=apk)
    asistencia_alumno.save()
    dictado = Dictado.objects.get(pk=pk)
    curso = Curso.objects.get(pk=dictado.curso.pk)
    return redirect('cursos:alumnos_dictado',curso.pk)   

def registrarAsistenciaProfesor(request, pk, ppk):
    titular = Titular.objects.filter(titular_dictado_pk=pk)
    asistencia_profesor = Asistencia_profesor(titular)
    asistencia_profesor.save()

class PagoAlumnoCreateView(CreateView):
    model = Pago_alumno
    form_class = FormularioPagoAlumno
    template_name = 'otro/pago_alumno_form.html'  
    success_url = reverse_lazy('cursos:cursos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de profesores"
        return context

class ProfesorDelDictadoListView(ListFilterView):
    model = Titular
    paginate_by = 100
    filter_class = ProfesorDelDictadoFilterForm
    
    def get_queryset(self):
          titular = super().get_queryset().filter(dictado__pk=self.kwargs['pk'])
          
          return titular

class agregarAlumnoCursoListView(ListFilterView):
    model = Alumno
    paginate_by = 100
    filter_class = AlumnosDelDictadoFilterForm

    def get_queryset(self):
          return super().get_queryset().filter(dictado__pk=self.kwargs['pk'])

def registrarAlumnoADictado(request, pk, apk):
    alumno = Alumno.objects.get(pk=apk)
    dictado = alumno.agregateDictado(pk)
    return redirect('cursos:alumnos_dictado', dictado.pk)

