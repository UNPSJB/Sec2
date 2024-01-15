from django import forms
from ..models import Curso, Actividad
from utils.constants import *
from utils.choices import *
from sec2.utils import FiltrosForm

#----------------------- CURSO --------------------
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('duracion', 'nombre', 'descripcion', 'es_convenio', 'area','requiere_certificado_medico')

    def __init__(self, *args, **kwargs):
        print("----------8-------------")
        super(CursoForm, self).__init__(*args, **kwargs)
        tipo_curso = kwargs.get('initial', {}).get('tipo_curso')
        # Configuración predeterminada
        print("ESTOY EN EL INIT")
        print(tipo_curso)

        if tipo_curso == 'convenio':
            print("----------9-------------")
            self.fields['area'].initial = 0
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['area'].required = False
        else:
            if tipo_curso == 'sec':
                print("----------10-------------")
                self.fields['area'].widget = forms.Select(choices=[(0, "Capacitación"), (1, "Cultura")])
                self.fields['area'].required = True
            else:
                if tipo_curso == 'actividad':
                    print("----------11-------------")
                    self.fields['area'].initial = 2
                    self.fields['area'].widget = forms.HiddenInput()
                    self.fields['area'].required = False
                else:
                    print("----------12-------------")
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
    duracion = forms.ChoiceField(
        label='Duración',
        choices=[('', '---------')] + list(DURACION),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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