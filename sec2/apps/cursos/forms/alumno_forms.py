from django import forms
from apps.cursos.models import Alumno
from apps.personas.models import Persona
from datetime import date

from sec2.utils import FiltrosForm

#-------------- Fusion de formulario Alumno y Persona----------------
class AlumnoPersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class AlumnoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)