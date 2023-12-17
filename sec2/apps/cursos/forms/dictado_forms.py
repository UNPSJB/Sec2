from django import forms
from apps.cursos.forms.titular_forms import *
from ..models import Dictado, Profesor
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

    class Meta:
        model = Dictado
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        minimo_alumnos = cleaned_data.get('minimo_alumnos')
        maximos_alumnos = cleaned_data.get('maximos_alumnos')
        if minimo_alumnos is not None and maximos_alumnos is not None:
            if minimo_alumnos >= maximos_alumnos:
                raise forms.ValidationError('El número mínimo de inscriptos debe ser menor que el máximo.')
        return cleaned_data


class DictadoFilterForm(FiltrosForm):
    fecha_inicio  = forms.DateField(required=False)
    fecha_fin =forms.DateField(required=False)
