from django.db import models
from apps.cursos.models import Dictado
from apps.personas.models import Persona, Rol
from django.utils import timezone
from utils.constants import *
from utils.regularexpressions import *

# -------------------- FAMILIAR ------------------
class Familiar(Rol):
    TIPO = 2  # Define un valor único para el tipo de rol de Familiar

    TIPOS_RELACION = (
        (1, "Esposo/a"),
        (2, "Hijo/a"),
        # (3, "Padre"),
        # (4, "Madre"),
        # (5, "Hermano"),
        # (6, "Tutor"),
    )

    tipo_relacion = models.PositiveSmallIntegerField(choices=TIPOS_RELACION)
    activo = models.BooleanField(default=False)  # Agregamos el campo "activo" con valor predeterminado True
    dictados = models.ManyToManyField(Dictado, related_name="familiares", blank=True)
    lista_espera = models.ManyToManyField(Dictado, related_name='familiares_en_espera', blank=True)
    
    def __str__(self):
        return f"Tipo: {self.get_tipo_display()} Relación: {self.get_tipo_relacion_display()} Activo: {self.activo}"

Rol.register(Familiar)
# -------------------- AFILIADO ------------------
class Afiliado(Rol):
    TIPO = 1

    ESTADO = (
        (1, "pendiente de aceptación"),
        (2, "activo"),
        (3, "inactivo"),
        )
    estado = models.PositiveSmallIntegerField(choices=ESTADO, default=1)  # Establece 1 como valor por defecto
    razon_social = models.CharField(max_length=30, validators=[text_and_numeric_validator])
    categoria_laboral = models.CharField(max_length=20, validators=[text_and_numeric_validator])
    rama = models.CharField(max_length=50, validators=[text_and_numeric_validator])
    sueldo= models.DecimalField(max_digits=9, decimal_places=2, validators=[validate_positive_decimal])

    def validate_fecha(value):
        if value > timezone.now().date():
            raise ValidationError('La fecha no puede ser en el futuro.')
    
    fechaAfiliacion= models.DateField(
        null=True,
        blank=False,
        validators=[validate_fecha]
    )
    fechaIngresoTrabajo = models.DateField(
        null=False,
        blank=False,
        validators=[validate_fecha]
    )
    cuit_empleador = models.CharField(max_length=11, validators=[numeric_validator], help_text='Cuit sin puntos y guiones. Ej: 01234567899')
    localidad_empresa = models.CharField(
        max_length=30,
        choices=LOCALIDADES_CHUBUT,
        default="TRELEW",
    )
    domicilio_empresa = models.CharField(max_length=50, validators=[text_and_numeric_validator], help_text='Calle y numero')
    horaJornada = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dictados = models.ManyToManyField(Dictado, related_name="afiliados", blank=True)
    lista_espera = models.ManyToManyField(Dictado, related_name='afiliados_en_espera', blank=True)
    familia = models.ManyToManyField(Familiar, through='RelacionFamiliar', blank=True)

    def __str__(self):
        return f"Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"
    
    def __strextra__(self):
        # Define your new string representation here
        return f"{self.persona.dni} | {self.persona}"
    
    def tiene_esposo(self):
        esposo_existente = self.familia.filter(tipo_relacion=1).exists()
        return esposo_existente

Rol.register(Afiliado)

class RelacionFamiliar(models.Model):
    afiliado = models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    familiar = models.ForeignKey(Familiar, on_delete=models.CASCADE)
    # tipo_relacion = models.PositiveSmallIntegerField(choices=Familiar.TIPOS_RELACION)


