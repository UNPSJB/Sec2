from django import forms
from django.shortcuts import get_object_or_404
from apps.cursos.forms.titular_forms import *
from ..models import Curso, Dictado, Profesor, Aula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from sec2.utils import FiltrosForm
from utils.constants import *

class DictadoForm(forms.ModelForm):
    profesor = forms.ModelChoiceField(
        queryset=Profesor.objects.all(),
        label='Profesor',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
    )

    fecha = forms.DateTimeField(
        label='Fecha de inicio',
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Dictado
        fields = '__all__'
        exclude = ['curso']

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Verificar si la fecha seleccionada es un domingo
        if fecha and fecha.weekday() == 6:  # 0 es lunes, 1 es martes, ..., 6 es domingo
            raise forms.ValidationError('No se permiten fechas que sean domingos.')

        # Verificar que los minutos sean 00, 15 o 30
        if fecha.minute not in [0, 15, 30]:
            raise forms.ValidationError('Los minutos deben ser 00, 15 o 30.')

        # Verificar el rango de horas entre las 9 am y las 8 pm (20:00)
        if not (9 <= fecha.hour < 20):
            raise forms.ValidationError('La hora debe estar entre las 9 am y las 8 pm.')

        return fecha
    

# class DictadoFilterForm(FiltrosForm):
#     fecha_inicio  = forms.DateField(required=False)
#     fecha_fin =forms.DateField(required=False)

