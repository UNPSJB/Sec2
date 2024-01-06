from django.db import models
from apps.personas.models import Rol
from utils.constants import *
from utils.regularexpressions import *
from django.core.validators import MinValueValidator, MaxValueValidator

# ---------------- ACTIVIDAD ---------------
class Actividad(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    descripcion = models.CharField(
        max_length=100,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Descripción del la actividad"
    )
    area = models.PositiveSmallIntegerField(choices=AREAS)

    def __str__(self):
        return self.nombre

# The line `#------------- CURSO --------------------` is a comment that serves as a visual separator
# or marker in the code. It helps to distinguish different sections or blocks of code for better
# readability and organization.
#------------- CURSO --------------------
class Curso(models.Model):

    actividad = models.ForeignKey(Actividad,related_name="cursos", on_delete=models.CASCADE)
    duracion = models.PositiveSmallIntegerField(choices=DURACION)
    #capacidad maxima de participantes para el curso
    capacidad_maxima= models.PositiveIntegerField(help_text="Máximo de inscriptos")
    nombre = models.CharField(
        max_length=50,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    descripcion = models.CharField(
        max_length=255,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Descripción del curso"
    )

    def __str__(self):
        return f"{self.nombre} {self.actividad}"
    
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
    nombre = models.CharField(
        max_length=50,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )

    #maximo de alumnos que se permiten inscribir.
    #Funciona de manera independiente al del curso, ya que cada profesor puede eleegir la cantidad
    maximos_alumnos = models.PositiveIntegerField(
        help_text="Máximo alumnos inscriptos",
        validators=[
            MinValueValidator(1, message="Valor mínimo permitido es 1."),
            MaxValueValidator(100, message="Valor máximo es 100."),
        ]
    )

    periodo_pago=models.PositiveSmallIntegerField(choices=PERIODO_PAGO)
    costo = models.DecimalField(
        help_text="Total del dictado",
        max_digits=10,
        decimal_places=0
    )
    certificado_medico=models.PositiveSmallIntegerField(choices=OPCIONES_CERTIFICADO)
    descuento = models.PositiveIntegerField(
        help_text="Descuento para afiliados",
        validators=[
            MinValueValidator(0, message="El descuento no puede ser menor que 0."),
            MaxValueValidator(100, message="El descuento no puede ser mayor que 100."),
        ]
    )
    cantidad_clase= models.PositiveIntegerField(help_text="Aproximado")
    minimo_alumnos= models.PositiveIntegerField(help_text="Para poder iniciar el dictado")
    # 1 modulo equivale a la cantidad de horas
    modulos= models.PositiveIntegerField(help_text="Horas del curso")
    curso = models.ForeignKey(Curso, related_name="dictado_set", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"HOLAAA!! SOY EL DICTADO : "

    def asignar_clase(self, fecha, hora_inicio):
        clase = Clase()
        clase.hora_inicio = hora_inicio
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
        return self.denominacionw

#------------- HORARIO --------------------
class Horario(models.Model):
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    aula = models.ForeignKey(Aula, related_name='horarios', on_delete=models.CASCADE)
    asistencia = models.PositiveIntegerField(default=0, help_text="Número de alumnos que asistieron")
    
    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.hora_inicio} - {self.aula}"
    
#------------- CLASE --------------------
class Clase(models.Model):
    dictado = models.ForeignKey(Dictado, related_name="clases", null=True, on_delete=models.CASCADE)
    nombre = models.CharField(
        max_length=50,  
        validators=[text_validator],
        help_text="Solo se permiten letras y espacios."
    )
    inscritos = models.PositiveIntegerField(default=0, help_text="Número de alumnos inscritos")
    horarios = models.ManyToManyField(Horario, related_name='clases')  # Agrega este campo

    def __str__(self):
        return self.nombre



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
