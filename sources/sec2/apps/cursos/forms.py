from django.forms import ModelForm, Textarea
from django import forms
from django.forms import ValidationError
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona
from .models import Actividad
from .models import Curso
from .models import Aula , Profesor , Dictado
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML


class DictadoForm(ModelForm):
    class Meta:
        model = Dictado
        fields = ['fecha_inicio','fecha_fin']

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




class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'
        #exclude=['persona', 'tipo']

        widgets ={
            
            'ejerce_desde': forms.DateInput(attrs={'type':'date'}),
            }
        
        labels = {
            'ejerce_desde': "Fecha en la empezo a ejercer el cargo de profesor"
        }

class FormularioProfesor(forms.ModelForm):
    fechaAfiliacion = forms.DateField()
    class Meta:
        model = Persona
        fields = '__all__'
        #exclude=['persona', 'tipo']
        help_texts = {
            'dni': 'Tu numero de documento sin puntos',
        }
        
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
        print(valid)
        print(personaForm.is_valid())
        print(profesorForm.is_valid())
        return valid and personaForm.is_valid() and profesorForm.is_valid()
    
    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        profesorForm = ProfesorForm(data=self.cleaned_data)
        profesor = profesorForm.save(commit=False)
        self.persona.convertir_en_profesor(Profesor)
        return profesor
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_action = 'Profesors:index'
        self.helper.layout = Layout(
            HTML(
                    '<h2><center>Formulario de Profesor</center></h2>'),
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
                   "Datos Academicos",
                HTML(
                    '<hr/>'),
                    'capacitaciones',
                    'ejerce_desde',
                    'actividades',
                    'dictados'
                    
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)


FormularioProfesor.base_fields.update(ProfesorForm.base_fields)

class DictadoForm(ModelForm):
    class Meta:
        model = Dictado
        fields = ['fecha_inicio','fecha_fin','aula']

        widgets ={   
            'fecha_inicio': forms.DateInput(attrs={'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date'}),
                }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                HTML(
                    '<h2><center>Formulario de Dictado</center></h2>'),
                Fieldset(
                    "Datos",
                    'fecha_inicio',
                    'fecha_fin','aula',
                ),
                Submit('submit', 'Guardar', css_class='button white'),)
