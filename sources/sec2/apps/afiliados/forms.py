from cProfile import label
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django.forms import ValidationError
from .models import Afiliado
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML


class AfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude=['persona', 'tipo']

        widgets ={
            
            'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'datetime-local'}),
            #'fechaAfiliacion': forms.DateInput(attrs={'type':'datetime-local'})
            }
        
        labels = {
            'fechaIngresoTrabajo': "fecha de ingreso al trabajo",
           # 'fechaAfiliacion': "Fecha de afiliacion"
        }
        
class FormularioAfiliado(forms.ModelForm):
    fecha_afiliacion = forms.DateField()
    class Meta:
        model = Persona
        fields = '__all__'
        exclude=['persona', 'tipo']
        help_texts = {
            'dni': 'Tu numero de documento!',
        }
        
        widgets ={
            
           'fecha_nacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
            #'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'datetime-local'}),
           # 'fecha_afiliacion': forms.DateInput(attrs={'type':'datetime-local'})
            }
        
        labels = {
           'fecha_nacimiento': "Fecha de nacimiento",
          # 'fecha_afiliacion': "Fecha de afiliacion"
           
        }

    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_afiliado:
            raise ValidationError("Ya existe un afiliado activo con ese DNI")
        return self.cleaned_data['dni']
        
    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and afiliadoForm.is_valid()
    
    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        afiliado = afiliadoForm.save(commit=False)
        self.persona.afiliar(afiliado, self.cleaned_data['fecha_afiliacion'])
        return afiliado
        #super().save(commit=commit)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            Fieldset(
                   "Datos Personales",
                HTML(
                    '<hr/>'),
                               
                    'dni', 
                    'nombre',
                    'apellido',
                    'fecha_nacimiento',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'celular',
                    
            ),
            Fieldset(
                   "Datos Laborales",
                HTML(
                    '<hr/>'),
                 HTML("""
            <p>Datos del empleador que te va a dar latigo</p>
        """),
                    'razon_social',
                    'cuit_empleador',
                    'domicilio_empresa',
                    'localidad_empresa',
                    'fechaIngresoTrabajo',
                    'rama',
                    'sueldo',
                    'horaJornada',
                   # 'fecha_afiliacion',
                    'categoria_laboral',        
            
            ),
            Submit('submit', 'Guardar', css_class='button white'),)


FormularioAfiliado.base_fields.update(AfiliadoForm.base_fields)

