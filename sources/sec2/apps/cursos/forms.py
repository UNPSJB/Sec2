from django.forms import ModelForm, Textarea
from django import forms
from django.forms import ValidationError
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona
from .models import Actividad
from .models import Aula, Profesor, Dictado, Curso, Clase, Titular
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm


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
                  'costo',
                  'nombre',
                  'modulos',
                  'requiere_certificado',
                  'dictado',
                  'periodo_pago',
                  'descuento'
                  ]
        exclude=['dictado']
    
    
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
                'costo',
                'nombre',
                'modulos',
                'requiere_certificado',
                'periodo_pago',
                'descuento',            ),
            Submit('submit', 'Guardar', css_class='button white'),Submit('submit', 'Guardar y Crear Dictado', css_class='button white'))




class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'
        exclude=['persona', 'tipo']

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
        self.persona.convertir_en_profesor(profesor)
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


class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = ['fecha_inicio','fecha_fin', 'aula']

        widgets ={   
            'fecha_inicio': forms.DateInput(attrs={'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date'}),
                }

    def save(self, curso, commit=False):
        # print('aca estoy')
        # print(self.cleaned_data)
        # formDictado = FormDictado(data=self.cleaned_data)
        fecha_inicio= self.cleaned_data["fecha_inicio"]
        fecha_fin= self.cleaned_data["fecha_fin"]
        aula = self.cleaned_data["aula"]
        curso.asignar_dictado(fecha_inicio, fecha_fin, aula)
        
        
        
       

    def __init__(self,initial=None, *args, **kwargs):
            curso = initial.pop('curso')
            print(curso)
            super().__init__(initial=initial,*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                HTML(
                    f'<h2><center>Alta de dictado para el curso {curso.nombre} </center></h2>'),
                Fieldset(
                    "Datos",
                    'fecha_inicio',
                    'fecha_fin','aula',
                ),
                Submit('submit', 'Guardar', css_class='button white'),)


class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    actividad = forms.ChoiceField(required=False)

class ActividadFilterForm(FiltrosForm):
    nombre  = forms.CharField(required=False)

class DictadoFilterForm(FiltrosForm):
    fecha_inicio  = forms.DateField(required=False)
    fecha_fin =forms.DateField(required=False)

    Submit('submit', 'Guardar', css_class='button white')
                
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['dia','hora_inicio','hora_fin']

        widgets ={   
            'hora_inicio': forms.DateInput(attrs={'type':'time'}),
            'hora_fin': forms.DateInput(attrs={'type':'time'}),
                }

    def save(self, dictado, commit=False):
        # print('aca estoy')
        # print(self.cleaned_data)
        hora_inicio= self.cleaned_data["hora_inicio"]
        hora_fin= self.cleaned_data["hora_fin"]
        dia = self.cleaned_data["dia"]
        # dictado = self.cleaned_data["dictado"]
        dictado.asignar_clase(dia, hora_inicio, hora_fin)

    def __init__(self, *args, **kwargs):
            #curso = kwargs.pop('curso')
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                HTML(
                    '<h2><center>Formulario de Clase</center></h2>'),
                Fieldset(
                    "Datos",
                    'dia',
                    'hora_inicio',
                    'hora_fin',
                ),
                Submit('submit', 'Guardar', css_class='button white'),)

class ClaseFilterForm (FiltrosForm):
    dia = forms.DateField(required=False)
    #actividad = forms.ChoiceField(required=False)

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude=['persona', 'tipo', 'dictado']


class FormularioAlumno (forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        help_texts = {
            'dni': 'Tu numero de documento sin puntos',
        }
        widgets ={
           'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
            }
        labels = {
           'fecha_nacimiento': "Fecha de nacimiento",
        }

    
    def save(self, curso, commit=False):
        # print(self.cleaned_data)
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
        except Persona.DoesNotExist:
            persona = None

        if persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            persona = personaForm.save()
        
        alumnoForm = AlumnoForm(data={'curso': curso})
        alumno = alumnoForm.save(commit=False)
        # curso = self.cleaned_data[""]
        persona.inscribir(alumno, curso)
        print("estoy aca")
        return alumno
        
        
    def __init__(self, instance=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                    '<h2><center>Formulario de Alumno</center></h2>'),
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
                   
                HTML(
                    '<hr/>'),
                    
                         
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)
