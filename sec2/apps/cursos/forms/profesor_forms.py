from django import forms
from django.forms import ValidationError
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from ..models import Profesor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'
        exclude=['persona', 'tipo', 'dictados']

        widgets ={
            
            'ejerce_desde': forms.DateInput(attrs={'type':'date'}),
            }
        
        labels = {
            'ejerce_desde': "Fecha en la empezo a ejercer el cargo de profesor"
        }

class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude=['persona', 'tipo']
        widgets ={
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
            }
        labels = {
            'fecha_nacimiento': "Fecha de nacimiento",
            }

    def clean_dni(self):
        print("ESTOY EN EL CLEAN_DNI")
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un Profesor activo con ese DNI")
        return self.cleaned_data['dni']

    def clean_cuil(self):
        print("ESTOY EN EL CLEAN CUIL")
        self.persona = Persona.objects.filter(dni=self.cleaned_data['cuil']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un Profesor activo con ese cuil")
        return self.cleaned_data['cuil']
        
    def is_valid(self) -> bool:
        print("ESTOY EN EL IS_VALID")
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        profesorForm = ProfesorForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and profesorForm.is_valid()
    
    def save(self, commit=False):
        print("ESTOY EN EL SAVE")
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        profesorForm = ProfesorForm(data=self.cleaned_data)
        profesor = profesorForm.save(commit=False)
        self.persona.convertir_en_profesor(profesor)
        return profesor
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

FormularioProfesor.base_fields.update(ProfesorForm.base_fields)

class ProfesorUpdateForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'
        exclude=['persona', 'tipo', 'dictados']

        widgets ={
            
           # 'ejerce_desde': forms.DateInput(attrs={'type':'date'}),
            }
        
        labels = {
            'ejerce_desde': "Fecha en la empezo a ejercer el cargo de profesor"
        }


class FormularioProfesorUpdateFrom(forms.Form):
           
    ##def clean_dni(self):
    ##    self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
    ##    if self.persona is not None and self.persona.es_profesor:
    ##        raise ValidationError("Ya existe un Profesor activo con ese DNI")
    ##    return self.cleaned_data['dni']

    ##def clean_cuil(self):
    ##    self.persona = Persona.objects.filter(dni=self.cleaned_data['cuil']).first()
    ##    if self.persona is not None and self.persona.es_profesor:
    ##        raise ValidationError("Ya existe un Profesor activo con ese cuil")
    ##    return self.cleaned_data['cuil']
        
    def is_valid(self) -> bool:
        sv = super().is_valid()
        pv = self.personaForm.is_valid()
        prov = self.profesorForm.is_valid()
        return sv and pv and prov
       
      ##  valid = super().is_valid()
      ##  personaForm = PersonaForm(data=self.cleaned_data)
      ##  profesorForm = ProfesorForm(data=self.cleaned_data)
      ##  return valid and personaForm.is_valid() and profesorForm.is_valid()
    
    def save(self, commit=False):
        self.personaForm.save()
        return self.profesorForm.save()
        
       ## if self.persona is None:
        ##    personaForm = PersonaForm(data=self.cleaned_data)
         ##   self.persona = personaForm.save()
       ## profesorForm = ProfesorForm(data=self.cleaned_data)
       ## profesor = profesorForm.save(commit=False)
       ## self.persona.convertir_en_profesor(profesor)
       ## return profesor
        
    def __init__(self, initial = {}, instance=None, *args, **kwargs):
       
        persona = instance.persona
        self.personaForm = PersonaUpdateForm(initial=initial, instance=instance.persona, *args, **kwargs)
        self.profesorForm = ProfesorUpdateForm(initial=initial, instance=instance, *args, **kwargs)
        initial = dict(self.personaForm.initial)
        initial.update(self.profesorForm.initial)
        super().__init__(initial=initial,*args, **kwargs)
        
        self.helper = FormHelper()
        #self.helper.form_action = 'Profesors:index'
        self.helper.layout = Layout(
            HTML(
                f'<h2><center>Modificar datos del Profesor {persona.nombre} {persona.apellido} </center></h2>'),
            Fieldset(
                   "Datos Personales",
                   
                HTML(
                    '<hr/>'),
                                             
                    #'dni', 
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
                   "Datos Academicos",
                HTML(
                    '<hr/>'),

                    'capacitaciones',
                    'ejerce_desde',
                    'actividades',
                    'dictados'
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)

FormularioProfesorUpdateFrom.base_fields.update(PersonaUpdateForm.base_fields)
FormularioProfesorUpdateFrom.base_fields.update(ProfesorUpdateForm.base_fields)

class ProfesorFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    # Area = models.PositiveSmallIntegerField()