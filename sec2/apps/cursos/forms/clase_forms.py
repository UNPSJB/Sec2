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
class CustomTimeInput(forms.TimeInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['minute_step'] = 30
        return context

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'
        exclude = ['dictado']
        widgets = {
            'hora_inicio': CustomTimeInput(attrs={'type': 'time', 'value': '00:00'}, format='%H:%M'),
        }

    def save(self, dictado, commit=False):
        fecha = self.cleaned_data["fecha"]
        hora_inicio = self.cleaned_data["hora_inicio"]
        dictado.asignar_clase(fecha, hora_inicio, hora_inicio)
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class ClaseFilterForm (FiltrosForm):
    dia = forms.DateField(required=False)
    #actividad = forms.ChoiceField(required=False)


