from django import forms
from django.shortcuts import get_object_or_404
from apps.cursos.forms.titular_forms import *
from ..models import Curso, Dictado, Profesor, Aula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from sec2.utils import FiltrosForm
from utils.constants import *

class DictadoForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que el campo 'profesor' está incluido en el formulario
        self.fields['profesor'] = forms.ModelChoiceField(
            queryset=Profesor.objects.all(),  # Ajusta el queryset según sea necesario
            required=False,  # Puedes ajustar esto según tus necesidades
            label='Profesor',  # Ajusta el label según sea necesario
        )

# class DictadoFilterForm(FiltrosForm):
#     fecha_inicio  = forms.DateField(required=False)
#     fecha_fin =forms.DateField(required=False)

