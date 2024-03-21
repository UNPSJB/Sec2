from django.db import models
from django.http import HttpResponse
from apps.personas.models import Rol
from utils.constants import *
from utils.choices import *
from utils.funciones import validate_no_mayor_actual
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

#------------- LISTA DE ESPERA --------------------
class ListaEspera(models.Model):
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='inscritos_lista_espera')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fechaInscripcion = models.DateTimeField(auto_now_add=True)
    
#------------- CURSO --------------------
class Curso(models.Model):
    # ForeignKey
    actividad = models.ForeignKey(Actividad, on_delete=models.SET_NULL, blank=True, null=True)
    lista_espera = models.ManyToManyField(ListaEspera, blank=True, related_name='cursos_en_lista_espera')  # Change the related_name here

    area = models.PositiveSmallIntegerField(choices=AREAS, blank=True, null=True)
    requiere_certificado_medico = models.BooleanField(default=False)
    requiere_equipamiento_informatico = models.BooleanField(default=False)
    es_convenio = models.BooleanField(default=False)
    modulos_totales= models.PositiveIntegerField(help_text="Horas totales del curso")    
    nombre = models.CharField(
        max_length=50,
        validators=[text_and_numeric_validator],
        help_text="Solo se permiten letras, números y espacios, con o sin tildes."
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
    cupo = models.PositiveIntegerField(
        help_text="Máximo alumnos inscriptos",
        validators=[
            MinValueValidator(1, message="Valor mínimo permitido es 1."),
            MaxValueValidator(100, message="Valor máximo es 100."),
        ],
        null=True,
    )
    
    fechaBaja= models.DateField(
        null=True,
        blank=False,
    )

    
    def __str__(self):
        return f"{self.nombre}"
    
    def get_tipo_curso(self):
        if self.es_convenio:
            return 'convenio'
        elif self.requiere_certificado_medico:
            return 'actividad'
        else:
            return 'sec'

#------------- DICTADO --------------------
class Dictado(models.Model):
    # ForeignKey
    curso = models.ForeignKey(Curso, related_name="dictado_set", on_delete=models.CASCADE, null=True, blank=True)
    
    modulos_por_clase= models.PositiveIntegerField(help_text="Horas por clase")
    asistencia_obligatoria = models.BooleanField(default=False)
    periodo_pago=models.PositiveSmallIntegerField(choices=PERIODO_PAGO)
    estado = models.PositiveSmallIntegerField(choices=ESTADO_DICTADO, default=1)
    fecha = models.DateTimeField(help_text="Seleccione la fecha de inicio")
    fecha_fin = models.DateTimeField(null=True,blank=True )
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
    # lista_espera = models.ManyToManyField('Dictado', related_name='alumnos_en_espera', blank=True)
    
    # Si realmente es un alumno o solo un interesado en algun curso
    es_potencial = models.BooleanField(default=True) 

    TIPO = ROL_TIPO_ALUMNO
    def agregar_dictado(self, dictado):
        if dictado.cupo > dictado.alumnos.count():
            self.dictados.add(dictado)
            return True
        else:
            # self.lista_espera.add(dictado)
            return False
    
    def esta_inscripto_o_en_espera(self, dictado):
        return dictado in self.dictados.all() 
    # or dictado in self.lista_espera.all()

    def esta_inscrito_en_dictado(self, dictado_pk):
        """
        Verifica si el alumno está inscrito en el dictado con la clave primaria dictado_pk.
        Devuelve True si está inscrito, False en caso contrario.
        """
        return self.dictados.filter(pk=dictado_pk).exists()

Rol.register(Alumno)

#------------- PROFESOR --------------------
class Profesor(Rol):
    # ForeignKey
    dictados = models.ManyToManyField(Dictado, through = "Titular", related_name="profesores", blank=True)
    TIPO = ROL_TIPO_PROFESOR
    actividades = models.ManyToManyField(Actividad, blank=True)
    dictados_inscriptos = models.ManyToManyField(Dictado, related_name="profesores_dictados_inscriptos", blank=True)
    # lista_espera = models.ManyToManyField(Dictado, related_name='profesores_en_espera', blank=True)

    ejerce_desde= models.DateField(
        null=True,
        blank=False,
        validators=[validate_no_mayor_actual]
    )

    def __str__(self):
        if self.persona_id and hasattr(self, 'persona'):
            return f"{self.persona.apellido} {self.persona.nombre}"
        else:
            return super().__str__()
Rol.register(Profesor)

#------------- CLASE --------------------
class Clase(models.Model):
    reserva = models.ForeignKey(Reserva, related_name="clases", on_delete=models.CASCADE, null=True, blank=True)
    #para que se procesa a tomar la asistencia de la siguiente clase
    asistencia_tomada = models.BooleanField(default=False)
    
    # Agregar un campo para registrar la asistencia de diferentes roles
    asistencia = models.ManyToManyField(Rol, related_name="asistencias", blank=True)
    asistencia_profesor = models.ManyToManyField(Profesor, related_name="asistencias_titular", blank=True)

    def marcar_asistencia(self, rol):
        # Verificar que la asistencia no se haya tomado antes
        if not self.asistencia_tomada:
            self.asistencia.add(rol)
            return True
        else:
            return False

    def tomar_asistencia(self):
        # Marcar la asistencia para la clase
        self.asistencia_tomada = True
        self.save()
    
    def tiene_asistencia(self, inscrito):
        return inscrito in self.asistencia.all()

from django.shortcuts import get_object_or_404
    
# Luego, podrías usar este método en tu vista para marcar la asistencia de un alumno, profesor, etc.
def marcar_asistencia(request, clase_id, rol_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    rol = get_object_or_404(Rol, pk=rol_id)

    if clase.marcar_asistencia(rol):
        return HttpResponse("Asistencia marcada correctamente.")
    else:
        return HttpResponse("Error: La asistencia ya ha sido tomada.")

#------------- TITULAR --------------------
class Titular(models.Model):
    # ForeignKey
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    dictado= models.ForeignKey(Dictado, on_delete=models.CASCADE)

class PagoProfesor(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='pagos_profesor')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0, 'El monto debe ser un valor positivo.')])
    desde = models.DateTimeField(auto_now_add=True)

# class Asistencia_profesor(models.Model):
#     fecha_asistencia_profesor = models.DateTimeField(auto_now_add=True)
#     titular = models.ForeignKey(Titular, related_name="asistencia_profesor", on_delete=models.CASCADE)

# class Pago_alumno(models.Model):
#     alumno = models.ForeignKey(Alumno, related_name="pago", on_delete=models.CASCADE)
#     fecha_pago_alumno = models.DateField()
#     monto= models.DecimalField(help_text="Monto pagado", max_digits=10, decimal_places=2)

#     def get_nombre_alumno(self):
#         return f'nombre de alumno: ({self.alumno.pk})'
