from django import forms
from ..models import Actividad
from sec2.utils import FiltrosForm
from utils.constants import *
from django import forms
##------------------ ACTIVIDAD --------------------
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = nombre.lower()
        return nombre

    def clean(self):
        pass

    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        # Modifica el campo nombre para que la primera letra sea mayúscula y el resto en minúscula
        actividad.nombre = actividad.nombre.capitalize()
        if commit:
            actividad.save()
        return actividad

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

## ------------ FILTRO PARA ACTIVIDAD --------------
class ActividadFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(
        label='Área',
        choices=[('', '---------')] + list(Actividad.AREAS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )