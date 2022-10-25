from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from .models import Afiliado
from apps.personas.forms import PersonaForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML

class AfiliadoForms(forms.ModelForm):
    
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude=['persona', 'tipo']
        Widgets ={
            
            'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'date'}),
            #'fechaAfiliacion': forms.DateInput(attrs={'type':'date'})
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
                    'razon_social',
                    'cuit_empleador',
                    'categoria_laboral',
                    'domicilio_empresa',
                    'localidad_empresa',
                    'rama',
                    'fechaIngresoTrabajo',
                    'sueldo',
                    'horaJornada',
                    'fechaAfiliacion',
           
            ),
            Submit('submit', 'Guardar', css_class='button white'),)


AfiliadoForms.base_fields.update(AfiliadoForms.base_fields)

