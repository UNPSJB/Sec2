from apps.personas.models import Persona, Vinculo
from django.forms import ModelForm, formset_factory, BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django_select2 import forms as s2forms


class PersonaForm(ModelForm):
   
    class Meta:
        model = Persona
        fields = '__all__'
        #exclude=['persona', 'tipo']
        Widgets ={
            'fechaNacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'guardarAfiliado'
        self.helper.layout = Layout(
            Fieldset(
                   "",
                HTML(
                    '<hr/>'),
                    'dni', 
                    'fechaNacimiento',
                    'nombre',
                    'apellido',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'celular',      
            
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

PersonaForm.base_fields.update(PersonaForm.base_fields)

class PersonaUpdateForm(ModelForm):
   
    class Meta:
        model = Persona
        exclude=['dni', "familia",'es_afiliado','es_alumno','es_profesor','es_encargado']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'guardarAfiliado'
        self.helper.layout = Layout(
            Fieldset(
                   "",
                HTML(
                    '<hr/>'),
                    'fecha_nacimiento',
                    'nombre',
                    'apellido',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'celular',      
            
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class PersonaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "dni__icontains",
        "nombre__icontains",
        "apellido__icontains",
    ]

class BuscadorPersonasForm(forms.Form):
   buscar = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=PersonaWidget)



class VinculoForm(forms.ModelForm):
    class Meta:
        model = Vinculo
        fields = ("tipoVinculo",
                  "vinculado")

class BaseVinculoFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Guardar'))

VinculoFormSet = formset_factory(VinculoForm, formset=BaseVinculoFormSet,
    extra=1,
)