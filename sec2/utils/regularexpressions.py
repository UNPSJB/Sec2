from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from utils.constants import *

numeric_validator = RegexValidator(
        regex=r'^\d+$',
        message=f'{XMARK_ICON} Debe contener solo dígitos numéricos.',
        code='invalid_numeric'
    )

text_validator = RegexValidator(
    regex=r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s.]+$',
    message=f'{XMARK_ICON} Debe contener letras, espacios',
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

def telefono_argentino_validator(value):
    if not value:
        return  # Permite valores vacíos, ya que eso debería ser manejado por otro validador si es necesario.

    # Acepta los formatos +549XXXXXXXXX, 0XX-XXXXXXXX, 15XXXXXXXXX.
    pattern = r'^(\+?549\d{9}|0\d{2}-\d{8}|15\d{8})$'
    if not RegexValidator(pattern)(value):
        raise ValidationError('Número de teléfono no válido para Argentina. Utilice el formato +549XXXXXXXXX, 0XX-XXXXXXXX o 15XXXXXXXXX.')

# Define una función para validar si el valor es un número
def is_numeric(value):
    return value.isnumeric()
