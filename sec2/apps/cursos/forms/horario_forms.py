from django import forms
from ..models import Horario
from utils.constants import *
from django import forms

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia_semana', 'hora_inicio', 'aula']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M')
        }