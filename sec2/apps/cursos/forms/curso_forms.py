from django import forms
from ..models import Curso
from utils.constants import *
from sec2.utils import FiltrosForm


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        return nombre

    def clean(self):
        pass

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    # actividad = forms.ChoiceField(required=False)
    periodo_pago = forms.ChoiceField(
        label='Periodo de pago',
        choices=[('', '---------')] + list(PERIODO_PAGO),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
