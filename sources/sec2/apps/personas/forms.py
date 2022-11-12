from apps.personas.models import Persona, Vinculo
from django.forms import ModelForm, formset_factory, BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms

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