from django import forms
from ..models import Horario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *

# ------------- FORMULARIO DE HORARIO --------------
class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'
        exclude = ['asistencia'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
