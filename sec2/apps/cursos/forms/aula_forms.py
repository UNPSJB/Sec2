from django import forms
from ..models import Aula
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *
from django.urls import reverse

## ------------ FORMULARIO DE AULA --------------
class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'

    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        tipo = tipo.lower()
        return tipo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

## ------------ FILTRO PARA AULA --------------
class AulaFilterForm(FiltrosForm):
    cupo = forms.CharField(required=False)