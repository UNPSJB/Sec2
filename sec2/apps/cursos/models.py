from django.db import models
from apps.personas.models import Rol
from utils.constants import *
from utils.regularexpressions import *

# ---------------- ACTIVIDAD ---------------
class Actividad(models.Model):
    AREAS = [
        (0, "Capacitación"),
        (1, "Cultura"),
        (2, "Gimnasio"),
    ]
    nombre = models.CharField(
        max_length=100,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    area = models.PositiveSmallIntegerField(choices=AREAS)
    
    def __str__(self):
        return self.nombre

#------------- CURSO --------------------
class Curso(models.Model):
    actividad = models.ForeignKey(Actividad,related_name="cursos", on_delete=models.CASCADE)
    costo = models.DecimalField(
        help_text="costo total del curso sin puntos",
        max_digits=10,
        decimal_places=0
    )
    nombre = models.CharField(
        max_length=50,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    # 1 modulo es igual a un tiempo que equivale la duración de cada clase
    modulos= models.PositiveIntegerField(help_text="cantidad de horas del curso")
    # se le dejara a los cursos de gimnasio obligatorio certificado medico
    certificado_medico = models.BooleanField()
    periodo_pago=models.PositiveSmallIntegerField(choices=PERIODO_PAGO)
    descuento=models.PositiveIntegerField(help_text="porcentaje de descuento")

    def __str__(self):
        return f"{self.nombre} {self.actividad} Precio:{self.costo}"
    
    def asignar_dictado(self, dictado):
        dictado.curso = self
        return dictado

    def obtenerDictados(self,curso): 
        dictados=[]
        for dictado in Dictado:
            dictadocurso=dictado.curso
            if (dictadocurso.pk == curso.pk ):
                dictados.append[dictadocurso]
        return dictados

#------------- DICTADO --------------------
class Dictado(models.Model):
    cantidad_clase= models.PositiveIntegerField(help_text="Cantidad total de clase")
    minimo_alumnos= models.PositiveIntegerField(help_text="Minimo de alumnos")
    max_alumnos= models.PositiveIntegerField(help_text="Minimo de alumnos")
    # nombre = models.CharField(
    #     max_length=50,
    #     validators=[text_validator],  # Añade tu validador personalizado si es necesario
    #     help_text="Solo se permiten letras y espacios."
    # )    
    # curso = models.ForeignKey(Curso, related_name="curso", on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, related_name="dictado_set", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"HOLAAA!! SOY EL DICTADO : "

    def asignar_clase(self, fecha, hora_inicio, hora_fin):
        clase = Clase()
        clase.hora_inicio = hora_inicio
        clase.hora_fin = hora_fin
        clase.fecha = fecha
        clase.dictado = self
        clase.save()

#------------- AULA --------------------
class Aula(models.Model):
    TIPO_CHOICES = [
        ('normal', 'Normal'),
        ('laboratorio', 'Laboratorio'),
        ('conferencia', 'Conferencia'),
        ('computacion', 'Computación'),
    ]
    denominacion = models.CharField(max_length=50, unique=True, help_text="Nombre o identificador del aula, ej: Aula 22, Laboratorio 1")
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, help_text="Tipo de aula")
    cupo = models.PositiveIntegerField(help_text="Capacidad máxima del aula")

    def __str__(self):
        return self.denominacion

#------------- CLASE --------------------
class Clase(models.Model):
    dictado = models.ForeignKey(Dictado, related_name="clase", null=True, on_delete=models.CASCADE)

    aula=models.ForeignKey(Aula, related_name="aula", on_delete=models.CASCADE, null=True)
    fecha = models.DateField()
    hora_inicio=models.TimeField() 
    hora_fin=models.TimeField() # SE calcula desde la hora inicio más el modulo del curso

class Alumno(Rol):
    TIPO = 3
    dictado = models.ForeignKey(Dictado, related_name="alumnos", on_delete=models.CASCADE, null=True)
    curso = models.ForeignKey(Curso, related_name="alumnos", null=False, on_delete=models.CASCADE)

    def agregateDictado(self, pk):
        dictado = Dictado.objects.get(pk=pk)
        self.dictado=dictado
        self.save()
        return dictado
    
    def esta_inscripto(self):
        return self.dictado is not None

Rol.register(Alumno)

class Profesor(Rol):
    TIPO = 2
    capacitaciones = models.CharField(max_length=50)
    ejerce_desde = models.DateField()
    actividades = models.ManyToManyField(Actividad, blank=True)
    dictados = models.ManyToManyField(Dictado, through = "Titular", related_name="profesores", blank=True)

    def __str__(self):
        return f"{self.persona.nombre} {self.persona.apellido}"

Rol.register(Profesor)

class Titular(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    dictado= models.ForeignKey(Dictado, on_delete=models.CASCADE)

class Asistencia_profesor(models.Model):
    fecha_asistencia_profesor = models.DateTimeField(auto_now_add=True)
    titular = models.ForeignKey(Titular, related_name="asistencia_profesor", on_delete=models.CASCADE)

class Pago_profesor(models.Model):
    fecha_pago_profesor = models.DateField()
    titular = models.ForeignKey(Titular, related_name="pagos", on_delete=models.CASCADE)
    monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

class Asistencia_alumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name="asistencia", on_delete=models.CASCADE)
    dictado = models.ForeignKey(Dictado, on_delete=models.CASCADE)
    fecha_asistencia_alumno = models.DateTimeField(auto_now_add=True)
    

class Pago_alumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name="pago", on_delete=models.CASCADE)
    fecha_pago_alumno = models.DateField()
    monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

    def get_nombre_alumno(self):
        return f'nombre de alumno: ({self.alumno.pk})'