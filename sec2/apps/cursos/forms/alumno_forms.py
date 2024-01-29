from django import forms
from apps.cursos.models import Alumno
from apps.personas.models import Persona
from datetime import date

# from apps.personas.forms import PersonaForm
# from apps.personas.models import Persona
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit, HTML
# from sec2.utils import FiltrosForm
# from utils.constants import *

########### Fuseion de Formulario de afiliado Utilizado para el AFILIADO CRATE VIEW ##############################################
class AlumnoPersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude=['persona', 'tipo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        edad = date.today().year - fecha_nacimiento.year
        if edad < 18 or edad >= 100:
            raise forms.ValidationError("Debes ser mayor de 18 años y menor de 100 años.")
        return fecha_nacimiento

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude=['persona', 'tipo', 'dictado']

class FormularioAlumno (forms.ModelForm):
    class Meta:
        model = Persona 
        fields = '__all__'
#         help_texts = {
#             'dni': 'Tu numero de documento sin puntos',
#         }
#         widgets ={
#            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
#             }
#         labels = {
#            'fecha_nacimiento': "Fecha de nacimiento",
#         }

    
#     def save(self, curso, commit=False):
#         try:
#             persona = Persona.objects.get(dni=self.cleaned_data['dni'])
#         except Persona.DoesNotExist:
#             persona = None

#         if persona is None:
#             personaForm = PersonaForm(data=self.cleaned_data)
#             persona = personaForm.save()
        
#         alumnoForm = AlumnoForm(data={'curso': curso})
#         alumno = alumnoForm.save(commit=False)
#         # curso = self.cleaned_data[""]
#         persona.inscribir(alumno, curso)
#         return alumno
        
        
#     def __init__(self,  initial=None, instance=None,*args, **kwargs):    
#         curso = initial.get('curso')
       
#         self.alumnoFrom = AlumnoForm(initial=initial, instance=instance, *args, **kwargs)
#         self.alumnoFrom.fields['curso'].initial = curso.pk
       
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             HTML(
#                     '<h2><center>Formulario de Alumno</center></h2>'),
#             Fieldset(
#                    "Datos Personales",
                   
#                 HTML(
#                     '<hr/>'),
                                             
#                     'dni', 
#                     'nombre',
#                     'apellido',
#                     'fecha_nacimiento',
#                     'direccion',
#                     'mail',
#                     'nacionalidad',
#                     'estado_civil',
#                     'cuil',
#                     'celular',
                    
#             ),
            
#             Fieldset(    

#                 HTML(
#                     '<hr/>'),
#             ),
            
#             Submit('submit', 'Guardar', css_class='button white'),)
        
# class AlumnoFilterForm(FiltrosForm):
#     persona__nombre = forms.CharField(required=False)
#     Submit('submit', 'Guardar', css_class='button white')