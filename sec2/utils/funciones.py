from django.utils import timezone
from django.forms import ValidationError
from django.contrib import messages

from utils.constants import ICON_CHECK, ICON_ERROR, ICON_TRIANGLE

# ------------- FUNCIONES PARA MENSAJES ------------------
def mensaje_error(request, message):
    messages.error(request, f'{ICON_ERROR} {message}')

def mensaje_exito(request, message):
    messages.success(request, f'{ICON_CHECK} {message}')

def mensaje_advertencia(request, message):
    messages.warning(request, f'{ICON_TRIANGLE} {message}')
#-----------------------------------------------------------

def validate_no_mayor_actual(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha no puede ser en el futuro.')



def handle_existing_person(self, form):
    dni = form.cleaned_data["dni"]
    messages.error(self.request, f'{ICON_ERROR} ERROR: Ya existe una persona registrada en el sistema con el mismo DNI.')
    return self.render_to_response(self.get_context_data(form=form))
