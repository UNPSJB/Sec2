from django import forms
from ..models import Curso, Actividad
from utils.constants import *
from sec2.utils import FiltrosForm


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        return nombre

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    actividad = forms.ModelChoiceField(
        label='Actividad',
        queryset=Actividad.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duracion = forms.ChoiceField(
        label='Duración',
        choices=[('', '---------')] + list(DURACION),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        try:
            return int(duracion)
        except (ValueError, TypeError):
            # Si no se puede convertir a un número, devuelve None
            return None