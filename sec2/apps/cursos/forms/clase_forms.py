from django import forms
from ..models import Clase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *

## ------------ FORMULARIO DE CLASE --------------
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'
        exclude=['dictado']
        widgets ={   
            'hora_inicio': forms.TimeInput(attrs={'type':'time'}),
            'hora_fin': forms.TimeInput(attrs={'type':'time'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, dictado, commit=False):
        hora_inicio = self.cleaned_data["hora_inicio"]
        hora_fin = self.cleaned_data["hora_fin"]
        fecha = self.cleaned_data["fecha"]
        dictado.asignar_clase(fecha, hora_inicio, hora_fin)
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<br> <h2 class="titulo"> {{ titulo }} </h2>'),
            Fieldset(
                "Datos",
                'fecha',
                'aula',
                'hora_inicio',
                'hora_fin',
            ),
            Submit('submit', 'Guardar', css_class='button white'),
            HTML('<a class="btn btn-secondary" href="{% url \'cursos:dictado\' dictado.pk %}">Cancelar</a>'),
        )

class ClaseFilterForm (FiltrosForm):
    dia = forms.DateField(required=False)
    #actividad = forms.ChoiceField(required=False)


