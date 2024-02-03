from audioop import reverse
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
# from ..models import Actividad, Curso, Dictado, Aula, Alumno, Asistencia_alumno, Asistencia_profesor, Titular
from django.shortcuts import get_object_or_404
from django.contrib import messages


def index(request):
    template = loader.get_template('home_curso.html')
    return HttpResponse(template.render())

# def registrarAsistenciaAlumno(request, pk, apk):
#     asistencia_alumno = Asistencia_alumno(dictado_id=pk, alumno_id=apk)
#     asistencia_alumno.save()
#     dictado = Dictado.objects.get(pk=pk)
#     curso = Curso.objects.get(pk=dictado.curso.pk)
#     return redirect('cursos:alumnos_dictado',curso.pk)   

# def registrarAsistenciaProfesor(request, pk, ppk):
#     titular = Titular.objects.filter(titular_dictado_pk=pk)
#     asistencia_profesor = Asistencia_profesor(titular)
#     asistencia_profesor.save()

# def registrarAlumnoADictado(request, pk, apk):
#     alumno = Alumno.objects.get(pk=apk)
#     dictado = alumno.agregateDictado(pk)
#     return redirect('cursos:alumnos_dictado', dictado.pk)

# def curso_eliminar(request, pk):
#     a = Curso.objects.get(pk=pk)
#     a.delete()
#     messages.success(request, f'<i class="fa-solid fa-square-check fa-beat-fade"></i>   El curso "{a.nombre}" se ha eliminado con éxito.')
#     return redirect('cursos:curso_listado') 

 

