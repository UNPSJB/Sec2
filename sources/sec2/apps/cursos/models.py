from django.db import models

# Create your models here.
from apps.personas.models import Rol

class Alumno(Rol):
    legajo = models.CharField(max_length=10)

Rol.register(Alumno)

class Actividades(models.Model):
    nombre=models.CharField(max_length=50)
    area=models.CharField(max_length=50)

class Curso(models.Model):
    actividad= models.models.models.ForeignKey(Actividades,related_name="cursos", on_delete=models.CASCADE)
    Costo=  models.DecimalField(help_text="costo total del curso", max_digits=10, decimal_places=2)
    Nombre=models.CharField(max_length=50)
    alumno=models.ManyToManyField(Alumno, related_name="inscripcion")
    modulos= models.PositiveIntegerField(help_text="cantidad de horas del curso")
    #requiere certificado [TRUE/FALSE]
    #dictado
    #inscripciones
    #cantidad de módulos
    #periodo pago [clase/mes]
    #descuento
    

class Profesor(Rol):
    TIPO = 2
    capacitaciones = models.CharField(max_length=50)
    ejerceDesde = models.DateField()
    actividades = models.models.ManyToManyField(Actividades)

