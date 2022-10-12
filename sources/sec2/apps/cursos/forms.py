from django.forms import ModelForm, Textarea
from django import forms
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona

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