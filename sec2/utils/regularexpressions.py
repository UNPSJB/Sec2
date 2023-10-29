from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from utils.constants import *

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

text_and_numeric_validator = RegexValidator(
        regex=r'^[A-Za-z0-9\s]+$',
        message=f'{XMARK_ICON} Sin caracteres especiales.',
        code='invalid_text'
    )

def validate_positive_decimal(value):
    if value < 0:
        raise ValidationError(f'{XMARK_ICON} El sueldo no puede ser un valor negativo.')

LOCALIDADES_CHUBUT = [
        ("COMODORO RIVADAVIA", "Comodoro Rivadavia"),
        ("RAWSON", "Rawson"),
        ("PUERTO MADRYN", "Puerto Madryn"),
        ("ESQUEL", "Esquel"),
        ("GAIMAN", "Gaiman"),
        ("TRELEW", "Trelew"),
    ]