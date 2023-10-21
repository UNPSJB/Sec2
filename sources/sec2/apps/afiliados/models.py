from django.db import models
from apps.personas.models import Rol
from datetime import date
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

XMARK_ICON = '<i class="fa-solid fa-xmark"></i>'

def validate_positive_decimal(value):
    if value < 0:
        raise ValidationError(f'{XMARK_ICON} El sueldo no puede ser un valor negativo.')
class Afiliado(Rol):
    TIPO = 1
    LOCALIDADES_CHUBUT = [
        ("COMODORO RIVADAVIA", "Comodoro Rivadavia"),
        ("RAWSON", "Rawson"),
        ("PUERTO MADRYN", "Puerto Madryn"),
        ("ESQUEL", "Esquel"),
        ("GAIMAN", "Gaiman"),
        ("TRELEW", "Trelew"),
    ]
    ESTADO = (
        (1, "pendiente de aceptación"), 
        (2, "activo"),
        (3, "inactivo"),
        )
    estado = models.PositiveSmallIntegerField(choices=ESTADO)
    text_and_numeric_validator = RegexValidator(
        regex=r'^[A-Za-z0-9\s]+$',
        message=f'{XMARK_ICON} Sin caracteres especiales.',
        code='invalid_text'
    )
    numeric_validator = RegexValidator(
        regex=r'^\d+$',
        message=f'{XMARK_ICON} Debe contener solo dígitos numéricos.',
        code='invalid_numeric'
    )
    text_validator = RegexValidator(
        regex=r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
        message=f'{XMARK_ICON} Debe contener letras y/o espacios.',
        code='invalid_text'
    )

    razon_social = models.CharField(max_length=30, validators=[numeric_validator,text_validator])
    categoria_laboral = models.CharField(max_length=20, validators=[text_and_numeric_validator])
    rama = models.CharField(max_length=50, validators=[text_and_numeric_validator])
    sueldo= models.DecimalField(max_digits=9, decimal_places=2, validators=[validate_positive_decimal])
    
    def validate_fecha(value):
        if value > timezone.now().date():
            raise ValidationError('La fecha no puede ser en el futuro.')
    
    fechaAfiliacion= models.DateField(
        null=False,
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

    def __str__(self):
        return self.nombre
        # return f"Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"

Rol.register(Afiliado)
