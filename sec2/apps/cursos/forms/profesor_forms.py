from django import forms
from django.forms import ValidationError
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from ..models import Actividad, Profesor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm

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
        print("ESTOY EN EL CLEAN CUIL")
        self.persona = Persona.objects.filter(dni=self.cleaned_data['cuil']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un Profesor activo con ese cuil")
        return self.cleaned_data['cuil']
        
    def is_valid(self) -> bool:
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
        model = Persona
        fields = '__all__'
        labels = {
            'fechaIngresoTrabajo': "Fecha de ingreso al trabajo",
            'fechaAfiliacion': "Fecha de afiliación",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        persona_fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        for field_name in persona_fields:
            if field_name == 'dni':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'cuil':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'nacionalidad':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'nombre':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'apellido':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'fecha_nacimiento':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'celular':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)

            if field_name == 'direccion':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'mail':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)
            if field_name == 'estado_civil':
                self.fields[field_name].initial = getattr(self.instance.persona, field_name)


## ------------ FILTRO DE PROFESOR --------------
class ProfesorFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    actividades = forms.ModelChoiceField(
        queryset=Actividad.objects.all(),
        required=False,
        empty_label="--------------",  # Texto para la opción vacía
    )