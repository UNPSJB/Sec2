from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from .models import Afiliado
from apps.personas.forms import PersonaForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML

class FormularioAfiliado(forms.ModelForm):
    
    
    
    
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude=['persona', 'tipo']
        Widgets ={
            'fechaNacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
            'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'date'}),
            'fechaAfiliacion': forms.DateInput(attrs={'type':'date'})
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
                    'nombre',
                    'apellido',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'cuil',
                    'celular',
                    'razon_social',
                    'cuit',
                    'categoria_laboral',        
            
            ),
            Submit('submit', 'Submit', css_class='button white'),)


FormularioAfiliado.base_fields.update(PersonaForm.base_fields)

