from django import forms
from ..models import Aula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *

## ------------ FORMULARIO DE AULA --------------
class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['denominacion', 'tipo', 'cupo']

    def clean_denominacion(self):
        denominacion = self.cleaned_data['denominacion']
        denominacion = denominacion.lower()
        return denominacion

    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        tipo = tipo.lower()
        return tipo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            
            Fieldset(
                "",
                'denominacion', 'tipo', 'cupo'
            ),
            Submit('submit', 'Guardar', css_class='button white'),
        )
        self.helper.form_method = 'post'

## ------------ FILTRO PARA AULA --------------
class AulaFilterForm(FiltrosForm):
    cupo = forms.CharField(required=False)