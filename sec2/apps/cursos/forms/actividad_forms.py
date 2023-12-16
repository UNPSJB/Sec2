from django import forms
from ..models import Actividad
from sec2.utils import FiltrosForm
from utils.constants import *
from django import forms
##------------------ ACTIVIDAD --------------------
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'  # Incluir todos los campos, incluido 'area'

    def clean(self):
        pass

    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        # Modifica el campo nombre para que la primera letra sea mayúscula y el resto en minúscula
        actividad.nombre = actividad.nombre
        if commit:
            actividad.save()
        return actividad

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hacer el campo 'area' disabled y agregar una clase de estilo para resaltar que no es editable
        self.fields['area'].widget.attrs['disabled'] = True
        self.fields['area'].widget.attrs['class'] = 'disabled-field'
        # Marcar el campo 'area' como no obligatorio
        self.fields['area'].required = False
## ------------ CREATE --------------
class ActividadCreateForm(ActividadForm):
    class Meta:
        model = Actividad
        fields = '__all__'  # Incluir todos los campos, incluido 'area'


## ------------ FILTRO PARA ACTIVIDAD --------------
class ActividadFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(
        label='Área',
        choices=[('', '---------')] + list(Actividad.AREAS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )