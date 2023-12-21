from django import forms
from ..models import Clase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *


class CustomTimeInput(forms.TimeInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Limita los minutos a "00" y "30"
        context['widget']['minute_step'] = 30

        return context

## ------------ FORMULARIO DE CLASE --------------
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'horarios']  # Agrega 'horarios' al conjunto de campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class ClaseFilterForm (FiltrosForm):
    dia = forms.DateField(required=False)
    #actividad = forms.ChoiceField(required=False)


