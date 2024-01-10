from django import forms
from django.forms import ValidationError
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from .models import Salon
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *


class SalonrForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ('nombre', 'localidad', 'direccion', 'capacidad', 'encargado', 'precio')
        widgets = {
           'nombre': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Nombre'}),
           'localidad': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'localidad'}),
           'direccion': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'direccion'}),
           'capacidad': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'capacidad'}),
           'encargado': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'encargado'}),
           'precio': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'precio'}),
       }
    
    #def __init__(self, *args, **kwargs):
     #   super().__init__(*args, **kwargs)
       # self.fields['localidad'].queryset = Localidad.objects.all()