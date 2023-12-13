from django import forms
from django.forms import ValidationError
from apps.cursos.models import Alumno
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from .models import Aula, Profesor, Dictado, Curso, Clase, Titular, Pago_alumno, Actividad
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *




##------------------ ACTIVIDAD --------------------
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

    def save(self, commit=True):
        actividad = super(ActividadForm, self).save(commit=False)
        # Modifica el campo nombre para que la primera letra sea mayúscula y el resto en minúscula
        actividad.nombre = actividad.nombre.capitalize()
        if commit:
            actividad.save()
        return actividad

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

## ------------ FILTRO PARA ACTIVIDAD --------------
class ActividadFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(
        label='Área',
        choices=[('', '---------')] + list(Actividad.AREAS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

## ------------ FORMULARIO DE AULA --------------
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h2><center>Formulario de Aulas</center></h2>'),
            Fieldset(
                "Datos",
                'denominacion', 'tipo', 'cupo'
            ),
            Submit('submit', 'Guardar', css_class='button white'),
        )
        self.helper.form_method = 'post'

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

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
        return valid and personaForm.is_valid() and profesorForm.is_valid()
    
    def save(self, commit=False):
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

class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = '__all__'
        # fields = ['fecha_inicio','fecha_fin', 'aula', 'precio']
        widgets ={   
            'fecha_inicio': forms.DateInput(attrs={'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date'}),
            }

class TitularForm(forms.ModelForm):
    class Meta:
        model = Titular
        fields = "__all__"
        exclude = ['dictado']


class FormularioDictado(forms.Form):
    def is_valid(self) -> bool:
        return super().is_valid()  and self.dictadoForm.is_valid() and self.titularForm.is_valid()

    def save(self, commit=False):
        curso = self.initial.get("curso")
        print("CURSOOO--")
        print(curso)
        dictado = self.dictadoForm.save(commit=False)
        titular = self.titularForm.save(commit=False)
        dictado = curso.asignar_dictado(dictado)
        dictado.save()
        titular.dictado = dictado
        titular.save()
        return dictado


    def __init__(self, initial=None, instance=None, *args, **kwargs):
        curso = initial.get('curso')
        self.dictadoForm = DictadoForm(initial=initial, instance=instance, *args, **kwargs)
        self.titularForm = TitularForm(initial=initial, *args, **kwargs)
        # self.dictadoForm.fields['precio'].initial = curso.costo
        # del self.dictadoForm.fields['curso']
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Datos",
                'cantidad_clase',
                'minimo_alumnos',
                'max_alumnos',
            ),
            Fieldset(
                "Titularidad",
                'profesor',
            ),
            Submit('submit', 'Guardar', css_class='button white'),
        )
FormularioDictado.base_fields.update(DictadoForm.base_fields)
FormularioDictado.base_fields.update(TitularForm.base_fields)


class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    # actividad = forms.ChoiceField(required=False)
    periodo_pago = forms.ChoiceField(
        label='Periodo de pago',
        choices=[('', '---------')] + list(PERIODO_PAGO),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )




class ProfesorFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    # Area = models.PositiveSmallIntegerField()
    
class DictadoFilterForm(FiltrosForm):
    fecha_inicio  = forms.DateField(required=False)
    fecha_fin =forms.DateField(required=False)

## ------------ FORMULARIO DE CLASE --------------
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'
        exclude=['dictado']
        widgets ={   
            'hora_inicio': forms.TimeInput(attrs={'type':'time'}),
            'hora_fin': forms.TimeInput(attrs={'type':'time'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, dictado, commit=False):
        hora_inicio = self.cleaned_data["hora_inicio"]
        hora_fin = self.cleaned_data["hora_fin"]
        fecha = self.cleaned_data["fecha"]
        dictado.asignar_clase(fecha, hora_inicio, hora_fin)
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h2 class="titulo"> {{ titulo }} </h2>'),
            Fieldset(
                "Datos",
                'fecha',
                'aula',
                'hora_inicio',
                'hora_fin',
            ),
            Submit('submit', 'Guardar', css_class='button white'),
            HTML('<a class="btn btn-secondary" href="{% url \'cursos:dictado\' dictado.pk %}">Cancelar</a>'),
        )

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
        return alumno
        
        
    def __init__(self,  initial=None, instance=None,*args, **kwargs):    
        curso = initial.get('curso')
       
        self.alumnoFrom = AlumnoForm(initial=initial, instance=instance, *args, **kwargs)
        self.alumnoFrom.fields['curso'].initial = curso.pk
       
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
class PagoAlumnoForms(forms.ModelForm):
    class Meta:
        model = Pago_alumno
        fields = '__all__'
       # exclude=['alumno']
        widgets ={
           'fecha_pago_alumno': forms.DateInput(attrs={'type':'date'}),
            }
        labels = {
           'fecha_pago_alumno': "Fecha de pago",
        }

class FormularioPagoAlumno(forms.Form):
    def is_valid(self) -> bool:
        return super().is_valid()   and self.pagoAlumnoForm.is_valid() and self.alumnoForm.is_valid()

    def save(self, commit=False):
       # dictado = alumno
        #profesor = pagoAlumno
        alumno = self.alumnoForm.save(commit=False)
        pagoAlumno = self.pagoAlumnoForm.save(commit=False)

       
        alumno.save()
        pagoAlumno.alumno = alumno
        pagoAlumno.save()
        return alumno

    def __init__(self, initial=None, instance=None, *args, **kwargs):
            self.alumnoForm = AlumnoForm(initial=initial, instance=instance, *args, **kwargs)
            self.pagoAlumnoForm = PagoAlumnoForms(initial=initial, *args, **kwargs)
            #self.dictadoForm.fields['precio'].initial = curso.costo
            super().__init__(initial=initial,*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                HTML(
                    f'<h2><center> Pago del alumno  </center></h2>'),
                Fieldset(
                    "Datos Pago",
                    'fecha_pago_alumno',
                    'monto',
                    ),

                
                Fieldset(
                    "Alumno",
                    'alumno',
                ),
                Submit('submit', 'Guardar', css_class='button white'),)

#FormularioPagoAlumno.base_fields.update(AlumnoForm.base_fields)
FormularioPagoAlumno.base_fields.update(PagoAlumnoForms.base_fields)

class AlumnosDelDictadoFilterForm(FiltrosForm):
    persona__nombre  = forms.CharField(required=False)
    persona__apellido =forms.CharField(required=False)

    Submit('submit', 'Guardar', css_class='button white')

class ProfesorDelDictadoFilterForm(FiltrosForm):
    profesor__persona__nombre  = forms.CharField(required=False)
    profesor__persona__apellido =forms.CharField(required=False)

    Submit('submit', 'Guardar', css_class='button white')
class AlumnoFilterForm(FiltrosForm):
    persona__nombre = forms.CharField(required=False)
    Submit('submit', 'Guardar', css_class='button white')

class AlumnosDelDictadoFilterForm(FiltrosForm):
    persona__nombre = forms.CharField(required=False)
    persona__dni  = forms.CharField(required=False)
