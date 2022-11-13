from random import choices
#from socket import TIPC_CONN_TIMEOUT
from django.db import models

# Create your models here.
from apps.personas.models import Rol

class Actividad(models.Model):
    AREAS = [
        (0, "Capacitación"),
        (1, "Cultura"),
        (2, "Gimnasio"),
    ]
    nombre = models.CharField(max_length=100)
    area = models.PositiveSmallIntegerField(choices=AREAS)

    def __str__(self):
        return self.nombre
    

class Aula(models.Model):
    denominacion=models.CharField(max_length=50)
    tipo=models.CharField(max_length=50)
    cupo=models.PositiveIntegerField(help_text="capacidad maxima del aula")

class Dictado(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    aula=models.ForeignKey(Aula, related_name="dictado", on_delete=models.CASCADE)

class Clase(models.Model):
    DIA=(
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miercoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sabado"),
        (7, "Domingo"),
    )
    dictado = models.ForeignKey(Dictado, related_name="clase", null=False, on_delete=models.CASCADE)
    dia=models.PositiveSmallIntegerField(choices=DIA)
    hora_inicio=models.TimeField(auto_now_add=True)
    hora_fin=models.TimeField(auto_now_add=True)

class Curso(models.Model):
    PERIODO_PAGO=(
        (1, 'mes'),
        (2, 'clase'),
    )
    actividad = models.ForeignKey(Actividad,related_name="cursos", on_delete=models.CASCADE)
    costo=  models.DecimalField(help_text="costo total del curso", max_digits=10, decimal_places=2)
    nombre=models.CharField(max_length=50)
    modulos= models.PositiveIntegerField(help_text="cantidad de horas del curso")
    requiere_certificado = models.BooleanField()
    dictado = models.ForeignKey(Dictado, related_name="cursos",on_delete=models.CASCADE, null=True, blank = True)
    periodo_pago=models.PositiveSmallIntegerField(choices=PERIODO_PAGO)
    descuento=models.PositiveIntegerField(help_text="porcentaje de descuento")

    def __str__(self):
        return f"{self.nombre} {self.actividad} Precio:{self.costo}"
    


class Alumno(Rol):
    legajo = models.CharField(max_length=10)
    dictado = models.ForeignKey(Dictado, related_name="alumnos", on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name="alumnos", null=False, on_delete=models.CASCADE)
    
    
Rol.register(Alumno)

class Profesor(Rol):
    TIPO = 2
    capacitaciones = models.CharField(max_length=50)
    ejerce_desde = models.DateField()
    actividades = models.ManyToManyField(Actividad, blank=True)
    dictados = models.ManyToManyField(Dictado, through = "Titular", related_name="profesores", blank=True)

Rol.register(Profesor)

class Titular(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    dicatdo= models.ForeignKey(Dictado, on_delete=models.CASCADE)

class Asistencia_profesor(models.Model):
    fecha_asistencia_profesor = models.DateField()
    titular = models.ForeignKey(Titular, related_name="asistencia_profesor", on_delete=models.CASCADE)

class Pago_profesor(models.Model):
    fecha_pago_profesor = models.DateField()
    titular = models.ForeignKey(Titular, related_name="pagos", on_delete=models.CASCADE)
    monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

class Asistencia_alumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name="asistencia", on_delete=models.CASCADE)
    fecha_asistencia_alumno = models.DateField()

class Pago_alumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name="pago", on_delete=models.CASCADE)
    fecha_pago_alumno = models.DateField()
    monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

