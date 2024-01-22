from django.db import models
from apps.personas.models import Rol
from utils.constants import *
from utils.choices import *
from utils.regularexpressions import *
from django.core.validators import MinValueValidator, MaxValueValidator

# ------------- AULA --------------------
class Aula(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPO_AULA, help_text="Tipo de aula")
    numero = models.PositiveIntegerField(help_text="Numero de aula")
    capacidad = models.PositiveIntegerField(help_text="Capacidad máxima del aula")
    # reservas = models.ManyToManyField('Reserva', related_name='aulas', blank=True)  # Make it optional
    # horarios = models.ManyToManyField('Horario', related_name='aulas')

    def clean(self):
        if self.numero <= 0:
            raise ValidationError({'numero': 'El número de aula debe ser mayor que 0.'})
        if self.capacidad <= 0:
            raise ValidationError({'cupo': 'La capacidad máxima del aula debe ser mayor que 0.'})

    def __str__(self):
        if self.tipo == 'normal':
            return 'Aula {}'.format(self.numero)
        return 'Computación {}'.format(self.numero)

# ------------- RESERVA --------------------
class Reserva(models.Model):
    fecha = models.DateTimeField()
    horarios = models.ManyToManyField('Horario', related_name='aulas')
    aula = models.ForeignKey(Aula, related_name="au_set", on_delete=models.CASCADE, null=True, blank=True)

#------------- CURSO --------------------
class Curso(models.Model):
    area = models.PositiveSmallIntegerField(choices=AREAS, blank=True, null=True)
    nombre = models.CharField(
        max_length=50,
        validators=[text_and_numeric_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    descripcion = models.CharField(
        max_length=255,
        validators=[text_and_numeric_validator],  # Añade tu validador personalizado si es necesario
        help_text="Descripción del curso"
    )
    costo = models.DecimalField(
        help_text="Costo total del curso",
        max_digits=10,
        decimal_places=0,
        blank=True,   # Set this to True to make the field optional
        null=True,    # Also set null to True if you want to allow NULL values in the database
        default=0     # Set the default value to 0
    )
    requiere_certificado_medico = models.BooleanField(default=False)
    es_convenio = models.BooleanField(default=False)
    modulos_totales= models.PositiveIntegerField(help_text="Horas totales del curso")    
    
    def __str__(self):
        return f"{self.nombre}"
    
    def get_tipo_curso(self):
        if self.es_convenio:
            print("SOY CONVENIO")
            return 'convenio'
        elif self.requiere_certificado_medico:
            print("SOY ACTIVIDAD")
            return 'actividad'
        else:
            print("SOY SEC")
            return 'sec'

#------------- DICTADO --------------------
class Dictado(models.Model):
    curso = models.ForeignKey(Curso, related_name="dictado_set", on_delete=models.CASCADE, null=True, blank=True)
    periodo_pago=models.PositiveSmallIntegerField(choices=PERIODO_PAGO)
    fecha = models.DateTimeField(help_text="Seleccione la fecha de inicio")
    cupo = models.PositiveIntegerField(
        help_text="Máximo alumnos inscriptos",
        validators=[
            MinValueValidator(1, message="Valor mínimo permitido es 1."),
            MaxValueValidator(100, message="Valor máximo es 100."),
        ]
    )

    descuento = models.PositiveIntegerField(
        help_text="Exclusivo para afiliados",
        validators=[
            MinValueValidator(0, message="El descuento no puede ser menor que 0."),
            MaxValueValidator(100, message="El descuento no puede ser mayor que 100."),
        ]
    )
    modulos_por_clase= models.PositiveIntegerField(help_text="Horas por clase")
    asistencia_obligatoria = models.BooleanField(default=False)

#------------- HORARIO --------------------
from datetime import datetime, timedelta

class Horario(models.Model):
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS_SEMANA_CHOICES)
    hora_inicio = models.TimeField(help_text="Ingrese la hora en formato de 24 horas (HH:MM)")
    dictado = models.ForeignKey(Dictado, related_name="horarios", null=True, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, related_name="horarios_rel", null=True, on_delete=models.SET_NULL)

    def calcular_hora_fin(self):
        # Calcular la hora de fin sumando los módulos por clase a la hora de inicio
        hora_inicio_datetime = datetime.combine(datetime.today(), self.hora_inicio)
        tiempo_modulo = timedelta(hours=self.dictado.modulos_por_clase)
        hora_fin_datetime = hora_inicio_datetime + tiempo_modulo
        return hora_fin_datetime.time()

#------------- CLASE --------------------
# class Clase(models.Model):
    # fecha = models.DateTimeField(help_text="Seleccione solo el día habilitado")
    # horario = models.ForeignKey(Horario, related_name="horario", null=True, on_delete=models.CASCADE)
    # aula = models.ForeignKey(Aula, related_name='clases', on_delete=models.CASCADE)
    # inscritos = models.PositiveIntegerField(default=0, help_text="Número de alumnos inscritos")


# class Alumno(Rol):
#     TIPO = 3
#     dictado = models.ForeignKey(Dictado, related_name="alumnos", on_delete=models.CASCADE, null=True)
#     curso = models.ForeignKey(Curso, related_name="alumnos", null=False, on_delete=models.CASCADE)

#     def agregateDictado(self, pk):
#         dictado = Dictado.objects.get(pk=pk)
#         self.dictado=dictado
#         self.save()
#         return dictado
    
#     def esta_inscripto(self):
#         return self.dictado is not None

# Rol.register(Alumno)

class Profesor(Rol):
    TIPO = 2
    # capacitaciones = models.CharField(max_length=50)
    ejerce_desde = models.DateField()
    # actividades = models.ManyToManyField(Actividad, blank=True)
    dictados = models.ManyToManyField(Dictado, through = "Titular", related_name="profesores", blank=True)

    def __str__(self):
        return f"{self.persona.nombre} {self.persona.apellido}"
Rol.register(Profesor)

class Titular(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    dictado= models.ForeignKey(Dictado, on_delete=models.CASCADE)




# class Asistencia_profesor(models.Model):
#     fecha_asistencia_profesor = models.DateTimeField(auto_now_add=True)
#     titular = models.ForeignKey(Titular, related_name="asistencia_profesor", on_delete=models.CASCADE)

# class Pago_profesor(models.Model):
#     fecha_pago_profesor = models.DateField()
#     titular = models.ForeignKey(Titular, related_name="pagos", on_delete=models.CASCADE)
#     monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

# class Asistencia_alumno(models.Model):
#     alumno = models.ForeignKey(Alumno, related_name="asistencia", on_delete=models.CASCADE)
#     dictado = models.ForeignKey(Dictado, on_delete=models.CASCADE)
#     fecha_asistencia_alumno = models.DateTimeField(auto_now_add=True)
    

# class Pago_alumno(models.Model):
#     alumno = models.ForeignKey(Alumno, related_name="pago", on_delete=models.CASCADE)
#     fecha_pago_alumno = models.DateField()
#     monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

#     def get_nombre_alumno(self):
#         return f'nombre de alumno: ({self.alumno.pk})'
