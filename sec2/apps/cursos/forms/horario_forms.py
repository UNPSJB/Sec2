from django import forms
from ..models import Horario
from utils.constants import *
from django import forms

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia_semana', 'hora_inicio', 'aula']

    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)
        self.fields['hora_inicio'].widget = forms.TimeInput(attrs={'class': 'tu-clase-css'})

    def clean(self):
        cleaned_data = super(HorarioForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super(HorarioForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

