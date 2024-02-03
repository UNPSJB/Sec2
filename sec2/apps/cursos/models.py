from django.db import models
from django.http import HttpResponse
from apps.personas.models import Rol
from utils.constants import *
from utils.choices import *
from utils.regularexpressions import *
from django.core.validators import MinValueValidator, MaxValueValidator

# ------------- ACTIVIDAD --------------------
class Actividad(models.Model):
    nombre = models.CharField(
        max_length=50,
        validators=[text_validator],  # Añade tu validador personalizado si es necesario
        help_text="Solo se permiten letras y espacios."
    )
    
    def __str__(self):
        return f"{self.nombre}"

# ------------- AULA --------------------
class Aula(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPO_AULA, help_text="Tipo de aula")
    numero = models.PositiveIntegerField(help_text="Numero de aula")
    capacidad = models.PositiveIntegerField(help_text="Capacidad máxima")

    def clean(self):
        if self.numero <= 0:
            raise ValidationError({'numero': 'El número de aula debe ser mayor que 0.'})
        if self.capacidad <= 0:
            raise ValidationError({'cupo': 'La capacidad máxima del aula debe ser mayor que 0.'})

    def __str__(self):
        if self.tipo == 'normal':
            return 'Aula {}'.format(self.numero)
        return 'Computación {}'.format(self.numero)
    
#------------- CURSO --------------------
class Curso(models.Model):
    # ForeignKey
    actividad = models.ForeignKey(Actividad, on_delete=models.SET_NULL, blank=True, null=True)

    area = models.PositiveSmallIntegerField(choices=AREAS, blank=True, null=True)
    requiere_certificado_medico = models.BooleanField(default=False)
    es_convenio = models.BooleanField(default=False)
    modulos_totales= models.PositiveIntegerField(help_text="Horas totales del curso")    
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
    # ForeignKey
    curso = models.ForeignKey(Curso, related_name="dictado_set", on_delete=models.CASCADE, null=True, blank=True)
    
    modulos_por_clase= models.PositiveIntegerField(help_text="Horas por clase")
    asistencia_obligatoria = models.BooleanField(default=False)
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

#------------- HORARIO --------------------
from datetime import datetime, timedelta

class Horario(models.Model):
    # ForeignKey
    dictado = models.ForeignKey(Dictado, related_name="horarios", null=True, on_delete=models.CASCADE)
    
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS_SEMANA_CHOICES)
    hora_inicio = models.TimeField(help_text="Ingrese la hora en formato de 24 horas (HH:MM)")
    hora_fin = models.TimeField(blank=True, null=True)
    #Utilizado para controlar que no se creen horarios antes del primer dictado creado
    es_primer_horario = models.BooleanField(default=False)  # Campo booleano con valor por defecto False

    def clean(self):
        if self.hora_inicio and self.dictado and self.dictado.modulos_por_clase:
            # Calcular la hora de fin al limpiar los datos del modelo
            hora_inicio_datetime = datetime.combine(datetime.today(), self.hora_inicio)
            tiempo_modulo = timedelta(hours=self.dictado.modulos_por_clase)
            hora_fin_datetime = hora_inicio_datetime + tiempo_modulo
            self.hora_fin = hora_fin_datetime.time()

    def calcular_hora_fin(self, hora_inicio, modulos_por_clase):
        # Calcular la hora de fin en cualquier otro lugar si es necesario
        if hora_inicio and modulos_por_clase:
            hora_inicio_datetime = datetime.combine(datetime.today(), hora_inicio)
            tiempo_modulo = timedelta(hours=modulos_por_clase)
            hora_fin_datetime = hora_inicio_datetime + tiempo_modulo
            return hora_fin_datetime.time()

# ------------- RESERVA --------------------
class Reserva(models.Model):
    # ForeignKey
    horario = models.ForeignKey(Horario, related_name="reservass", on_delete=models.CASCADE, null=True, blank=True)
    aula = models.ForeignKey(Aula, related_name="reservas", on_delete=models.CASCADE, null=True, blank=True)
    
    fecha = models.DateField()

#------------- ALUMNO --------------------
class Alumno(Rol):
    # ForeignKey
    dictados = models.ManyToManyField(Dictado, related_name="alumnos", blank=True)

    TIPO = 3
    def agregateDictado(self, pk):
        dictado = Dictado.objects.get(pk=pk)
        self.dictados.add(dictado)
        return dictado

    def esta_inscripto(self, dictado):
        return dictado in self.dictados
    
Rol.register(Alumno)

#------------- CLASE --------------------
from django.shortcuts import get_object_or_404
    
def marcar_asistencia(request, clase_id, alumno_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    alumno = get_object_or_404(Alumno, pk=alumno_id)

    if alumno in clase.reserva.aula.curso.alumnos.all():  # Verifica que el alumno esté inscrito en el curso
        clase.asistencia.add(alumno)
        # Puedes realizar otras acciones aquí, como guardar el registro en la base de datos
        return HttpResponse("Asistencia marcada correctamente.")
    else:
        return HttpResponse("Error: El alumno no está inscrito en este curso.")
    
class Clase(models.Model):
    reserva = models.ForeignKey(Reserva, related_name="clases", on_delete=models.CASCADE, null=True, blank=True)
    asistencia = models.ManyToManyField(Alumno, related_name="clases_asistidas", blank=True)
    asistencia_tomada = models.BooleanField(default=False)



#------------- PROFESOR --------------------
class Profesor(Rol):
    # ForeignKey
    dictados = models.ManyToManyField(Dictado, through = "Titular", related_name="profesores", blank=True)

    TIPO = 2
    # capacitaciones = models.CharField(max_length=50)
    ejerce_desde = models.DateField()
    # actividades = models.ManyToManyField(Actividad, blank=True)

    def __str__(self):
        return f"{self.persona.nombre} {self.persona.apellido}"


Rol.register(Profesor)

#------------- TITULAR --------------------
class Titular(models.Model):
    # ForeignKey
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
