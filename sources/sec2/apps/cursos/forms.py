from django.forms import ModelForm, Textarea
from django import forms
from django.forms import ValidationError
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona
from .models import Actividad
from .models import Curso
from .models import Aula
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

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['denominacion', 'tipo', 'cupo']

    def clean_denominacion(self):
        denominacion = self.cleaned_data['denominacion']
        denominacion = denominacion.lower()
        return denominacion

    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        tipo = tipo.lower()
        return tipo
    
    def clean(self):
        pass

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                '<h2><center>Formulario de Aulas</center></h2>'),
            Fieldset(
                "Datos",
                'denominacion', 'tipo', 'cupo'
            ),
            Submit('submit', 'Guardar', css_class='button white'),)


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
            HTML(
                '<h2><center>Formulario de Actividades</center></h2>'),
            Fieldset(
                "Datos",
                'nombre', 'area',
            ),
            Submit('submit', 'Guardar', css_class='button white'),)


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
                  'actividad',
                  'Costo',
                  'Nombre',
                  'modulos',
                  'requiere_certificado',
                  'dictado',
                  'periodo_pago',
                  'descuento'
                  ]

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
            HTML(
                '<h2><center>Formulario de Cursos</center></h2>'),
            Fieldset(
                "Datos",
                'actividad',
                  'Costo',
                  'Nombre',
                  'modulos',
                  'requiere_certificado',
                #   'dictado',
                  'periodo_pago',
                  'descuento',            ),
            Submit('submit', 'Guardar', css_class='button white'),)
