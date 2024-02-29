from django.utils import timezone
from django.forms import ValidationError

def validate_no_mayor_actual(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')
