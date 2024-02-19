from django.db import models
from apps.personas.models import Persona, Rol
from django.utils import timezone
from utils.constants import *
from utils.regularexpressions import *

class Familiar(models.Model):
    TIPOS = (
        (1, "Esposo/a"),
        (2, "Hijo/a"),
        # (3, "Padre"),
        # (4, "Madre"),
        # (5, "Hermano"),
        # (6, "Tutor"),
    )
    # AFILIADO = [1, 2, 3, 4, 5]
    # ALUMNO = [3, 4, 6]
    tipo=models.PositiveSmallIntegerField(choices=TIPOS)
    persona=models.ForeignKey(Persona, related_name = "familiares", on_delete = models.CASCADE) 
    activo = models.BooleanField(default=True)  # Agregamos el campo "estado" con valor predeterminado True

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
    familia = models.ManyToManyField(Familiar, blank=True)
    
    def __str__(self):
        return f"Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"
    
Rol.register(Afiliado)