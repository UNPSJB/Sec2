from datetime import timezone
from django import forms
from django.forms import ValidationError
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from utils.constants import ESTADO_CIVIL, MAX_LENGTHS, NACIONALIDADES
from ..models import Actividad, Profesor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm

## ------------ FORMULARIO DE PROFESOR --------------
class ProfesorPersonaForm(forms.ModelForm):
    ejerce_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    actividades = forms.ModelMultipleChoiceField(
        queryset=Actividad.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Puedes ajustar esto según tus necesidades
    )

    class Meta:
        model = Persona
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

########### PROFESOR UPDATE ##############################################
class ProfesorUpdateForm(forms.ModelForm):

    class Meta:
        model = Profesor
        fields = '__all__'
        exclude = ['tipo', 'hasta', 'persona']
        labels = {
            'ejerce_desde': "Fecha desde que empezo a ejercer",
        }

    def __init__(self, *args, **kwargs):
        super(ProfesorUpdateForm, self).__init__(*args, **kwargs)
        persona_fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        for field_name in persona_fields:
            if field_name == 'fecha_nacimiento':
                self.fields[field_name] = forms.DateField(
                    required=True,
                    initial=getattr(self.instance.persona, field_name),
                )
            elif field_name == 'estado_civil':
                self.fields[field_name] = forms.ChoiceField(
                    choices=ESTADO_CIVIL,
                    required=True,
                    initial=getattr(self.instance.persona, field_name),
                )
            elif field_name == 'nacionalidad':
                self.fields[field_name] = forms.ChoiceField(
                    choices=NACIONALIDADES,
                    required=True,
                    initial=getattr(self.instance.persona, field_name),
                )
            elif field_name in MAX_LENGTHS:
                max_length = MAX_LENGTHS[field_name]
                self.fields[field_name] = forms.CharField(
                    max_length=max_length,
                    required=True,
                    initial=getattr(self.instance.persona, field_name),
                    help_text=getattr(self.instance.persona._meta.get_field(field_name), 'help_text', '')
                )
            else:
                self.fields[field_name] = forms.CharField(
                    required=True,
                    initial=getattr(self.instance.persona, field_name),
                    help_text=getattr(self.instance.persona._meta.get_field(field_name), 'help_text', '')
                )
            self.fields[field_name].widget.attrs['readonly'] = False



## ------------ FORMULARIO DE PROFESOR --------------
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
    actividades = forms.ModelMultipleChoiceField(
    queryset=Actividad.objects.all(),
    widget=forms.CheckboxSelectMultiple,  # Este widget permite la selección múltiple
    required=False  # Puedes ajustar esto según tus necesidades
    )

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
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un Profesor activo con ese DNI")
        return self.cleaned_data['dni']

    def clean_cuil(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['cuil']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un Profesor activo con ese cuil")
        return self.cleaned_data['cuil']
        
    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        profesorForm = ProfesorForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and profesorForm.is_valid()
    
    # def save(self, commit=False):
    #     if self.persona is None:
    #         personaForm = PersonaForm(data=self.cleaned_data)
    #         # self.persona = personaForm.save()
    #     profesorForm = ProfesorForm(data=self.cleaned_data)
    #     profesor = profesorForm.save(commit=False)
    #     self.persona.convertir_en_profesor(profesor)
    #     return profesor
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
FormularioProfesor.base_fields.update(ProfesorForm.base_fields)




## ------------ FILTRO DE PROFESOR --------------
class ProfesorFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    actividades = forms.ModelChoiceField(
        queryset=Actividad.objects.all(),
        required=False,
        empty_label="--------------",  # Texto para la opción vacía
    )