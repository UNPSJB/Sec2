from django.forms import ModelForm, Textarea
from django import forms
from django.forms import ValidationError
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona
from .models import Actividad
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML

class AlumnoForm(ModelForm):
    #curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    curso = forms.CharField()

    class Meta:
        model = Alumno
        fields = "__all__"

    def save(self, commit=False):
        curso = self.cleaned_data["curso"]
        persona = Persona(**self.cleaned_data)
        alumno = self.save(commit=False)
        persona.registrar_en_curso(alumno, curso)

AlumnoForm.base_fields.update(PersonaForm.base_fields)

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'area']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = nombre.lower()
        return nombre

    def clean(self):
        pass

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre', 'area',
            Submit('submit', 'Guardar', css_class='button white'),)
