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
        fields = ['nombre'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

class ClaseFilterForm (FiltrosForm):
    dia = forms.DateField(required=False)
    #actividad = forms.ChoiceField(required=False)