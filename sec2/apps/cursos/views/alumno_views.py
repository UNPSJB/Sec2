# from ..models import Alumno
from ..forms.alumno_forms import *
from ..forms.curso_forms import *
from ..forms.dictado_forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sec2.utils import ListFilterView
from django.shortcuts import redirect


# class AlumnosListView(ListFilterView):
#     model = Alumno
#     paginate_by = 100
#     filter_class = AlumnoFilterForm
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["curso"] = self.kwargs['pk']
#         return context
    
#     def get_queryset(self):
#         return super().get_queryset().filter(curso__pk=self.kwargs['pk'])


# class AlumnoCreateView(CreateView):
#     model = Alumno
#     form_class = FormularioAlumno
#     success_url = reverse_lazy('cursos:cursos')

#     def get_initial(self,*args, **kwargs):
#         curso= Curso.objects.get(pk=self.kwargs.get("pk"))
#         return {'curso':curso}
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         curso = Curso.objects.get(id = self.kwargs.get('pk'))
#         context['curso'] = curso
#         return context
    
#     def post(self, *args, **kwargs):
#         form = self.get_form()
#         curso = Curso.objects.get(pk=self.kwargs.get("pk"))
#         if form.is_valid():
            
#             form.save(curso)
#         else: 
#             return redirect(self.success_url)

#     def alumno_inscribir(request, pk):
#          a = Alumno.objects.get(pk=pk)
#          return redirect('cursos:ver_inscriptos')
#     # def alumno_inscribir(request, pk):
#     #     a = Alumno.objects.get(pk=pk)
#     #     return redirect('cursos:ver_inscriptos')

#     # def get_initial(self,*args, **kwargs):
#     #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
#     #     return {'dictado':dictado}
    
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
#     #     context['dictado'] = dictado
#     #     return context
    
#     # def post(self, *args, **kwargs):
#     #     form = self.get_form()
#     #     dictado = Dictado.objects.get(pk=self.kwargs.get("pk"))
#     #     return redirect(self.success_url)

   
# # class AlumnosListView(ListView):
# #     model = Alumno
# #     paginate_by = 100
    
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context['dictado'] = Alumno.objects.get(id = self.kwargs.get('pk'))
# #         return context

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