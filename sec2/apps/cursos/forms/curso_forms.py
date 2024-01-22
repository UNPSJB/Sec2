from django import forms
from ..models import Curso
from utils.constants import *
from utils.choices import *
from sec2.utils import FiltrosForm

#----------------------- CURSO --------------------
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        exclude= ['es_convenio', ]

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        tipo_curso = kwargs.get('initial', {}).get('tipo_curso')
        # Configuración predeterminada

        if tipo_curso == 'convenio':
            self.fields['area'].initial = 0
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['area'].required = False
            self.fields['costo'].initial = 0
        else:
            if tipo_curso == 'sec':
                self.fields['area'].widget = forms.Select(choices=[(0, "Capacitación"), (1, "Cultura")])
                self.fields['area'].required = True
            else:
                if tipo_curso == 'actividad':
                    self.fields['area'].initial = 2
                    self.fields['area'].widget = forms.HiddenInput()
                    self.fields['area'].required = False
                else:
                    self.fields['area'].widget = forms.Select(choices=AREAS)
                    self.fields['area'].required = True

class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(
        label='Área',
        choices=[('', '---------')] + list(AREAS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # duracion = forms.ChoiceField(
    #     label='Duración',
    #     choices=[('', '---------')] + list(DURACION),
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    es_convenio = forms.BooleanField(
        label='Conv. Provincial',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        try:
            return int(duracion)
        except (ValueError, TypeError):
            # Si no se puede convertir a un número, devuelve None
            return None