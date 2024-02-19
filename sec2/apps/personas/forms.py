from apps.personas.models import Persona
from django.forms import ModelForm, modelformset_factory, ValidationError, BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django_select2 import forms as s2forms

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude=['persona', 'tipo']
        Widgets ={
            'fechaNacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
PersonaForm.base_fields.update(PersonaForm.base_fields)

class PersonaUpdateForm(ModelForm):
    class Meta:
        model = Persona  # Asocia el formulario al modelo Persona
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PersonaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "dni__icontains",
        "nombre__icontains",
        "apellido__icontains",
    ]

class BuscadorPersonasForm(forms.Form):
   buscar = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=PersonaWidget)