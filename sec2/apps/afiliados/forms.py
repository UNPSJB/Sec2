from cProfile import label
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django.forms import ValidationError
from .models import Afiliado
from apps.personas.forms import PersonaForm
from apps.personas.forms import PersonaUpdateForm
from apps.personas.models import Persona
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django.forms.models import model_to_dict
from sec2.utils import FiltrosForm
from django.core.validators import RegexValidator
from datetime import date, timedelta
from utils.regularexpressions import *
from utils.constants import *
from django.utils import timezone
import re


########### Utilizado para el AFILIADO CRATE VIEW ##############################################
class AfiliadoPersonaForm(forms.ModelForm):
    # Campos específicos del afiliado
    razon_social = forms.CharField(max_length=30, validators=[text_and_numeric_validator])
    categoria_laboral = forms.CharField(max_length=20, validators=[text_and_numeric_validator])
    rama = forms.CharField(max_length=50, validators=[text_and_numeric_validator])
    sueldo = forms.DecimalField(max_digits=9, decimal_places=2, validators=[validate_positive_decimal])
    fechaAfiliacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fechaIngresoTrabajo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    cuit_empleador = forms.CharField(max_length=11, validators=[numeric_validator], help_text='Cuit sin puntos y guiones. Ej: 01234567899')
    localidad_empresa = forms.ChoiceField(choices=LOCALIDADES_CHUBUT, initial="TRELEW")
    domicilio_empresa = forms.CharField(max_length=50, validators=[text_and_numeric_validator], help_text='Calle y numero')
    horaJornada = forms.IntegerField(validators=[MinValueValidator(1)])

    def clean_fechaAfiliacion(self):
        fecha_afiliacion = self.cleaned_data.get('fechaAfiliacion')
        if fecha_afiliacion > timezone.now().date():
            raise forms.ValidationError('La fecha de afiliación no puede ser en el futuro.')
        return fecha_afiliacion

    def clean_fechaIngresoTrabajo(self):
        fecha_ingreso_trabajo = self.cleaned_data.get('fechaIngresoTrabajo')
        if fecha_ingreso_trabajo > timezone.now().date():
            raise forms.ValidationError('La fecha de ingreso al trabajo no puede ser en el futuro.')
        return fecha_ingreso_trabajo
    class Meta:
        model = Persona
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        # labels = {
            # 'fechaIngresoTrabajo': "Fecha de ingreso al trabajo",
            # 'fechaAfiliacion': "Fecha de afiliación"
        # }

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        edad = date.today().year - fecha_nacimiento.year
        if edad < 18 or edad >= 100:
            raise forms.ValidationError("Debes ser mayor de 18 años y menor de 100 años.")
        return fecha_nacimiento

########### Utilizado para el AFILIADO fliadosListView ##############################################
class AfiliadoFilterForm(FiltrosForm):
    persona__nombre = forms.CharField(required=False)
    persona__dni = forms.CharField(required=False)
    cuit_empleador = forms.CharField(required=False)

########### Utilizado para el AFILIADO UPDATE ##############################################
class AfiliadoUpdateForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude = ['tipo', 'hasta', 'estado', 'persona']
        widgets = {
            # 'fechaAfiliacion': forms.DateInput(attrs={'type': 'date'}),
            # 'fechaIngresoTrabajo': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fechaIngresoTrabajo': "Fecha de ingreso al trabajo",
            'fechaAfiliacion': "Fecha de afiliación",
        }

    def __init__(self, *args, **kwargs):
        super(AfiliadoUpdateForm, self).__init__(*args, **kwargs)
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
            self.fields[field_name].widget.attrs['readonly'] = False  # P

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']

        if fecha_nacimiento > timezone.now().date():
            raise forms.ValidationError('La fecha de nacimiento no puede estar en el futuro.')

        return fecha_nacimiento

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if not nombre.isalpha():
            raise forms.ValidationError('El nombre debe contener solo letras y espacios.')

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']

        if not apellido.isalpha():
            raise forms.ValidationError('El apellido debe contener solo letras y espacios.')

        return apellido

    def clean_mail(self):
        mail = self.cleaned_data['mail']
        # Expresión regular para validar una dirección de correo electrónico
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, mail):
            raise forms.ValidationError('El correo electrónico no es válido.')

        return mail


    def clean_celular(self):
        celular = self.cleaned_data['celular']

        if not re.match(r'^\d{3}-\d{8}$', celular):
            raise forms.ValidationError('El número de celular debe tener el formato correcto (###-########).')

        return celular

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']

        # Agrega tus propias validaciones de dirección si es necesario
        if not direccion.isalnum():
            raise forms.ValidationError('La dirección no es válida.')

        return direccion

    def save(self, commit=True):
        # Actualiza los campos de Afiliado
        afiliado = super().save(commit=False)
        # No olvides guardar los campos de Afiliado aquí, si es necesario
        if commit:
            afiliado.save()

        return afiliado

    def is_valid(self):
        return super(AfiliadoUpdateForm, self).is_valid()

    def clean(self):
        cleaned_data = super(AfiliadoUpdateForm, self).clean()
        return cleaned_data

####-------------------------------------------
class AfiliadoVer(forms.ModelForm):
    fechaAfiliacion = forms.DateField()

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['familia']
        widgets = {
            # 'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
        }

        labels = {
            'fecha_nacimiento': "Fecha de nacimiento",
        }

    # ** SE COMENTO ESTA LINEA PARA QUE NO LO CHEQUEARA
    # def clean_dni(self):
    #     self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
    #     if self.persona is not None and self.persona.es_afiliado:
    #         raise ValidationError("Ya existe un afiliado activo con ese DNI")
    #     return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaUpdateForm(data=self.cleaned_data)
        afiliadoForm = AfiliadoUpdateForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and afiliadoForm.is_valid()

    def save(self, commit=False):
        if self.persona is None:
            personaForm = PersonaUpdateForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        afiliadoForm = AfiliadoUpdateForm(data=self.cleaned_data)
        afiliado = afiliadoForm.save(commit=False)
        self.persona.afiliar(afiliado, self.cleaned_data['fechaAfiliacion'])
        return afiliado

    def __init__(self, instance=None, *args, **kwargs):
        # model_to_dict(instance)
        if instance is not None:
            persona = instance.persona
            afiliado = instance.afiliado
            datapersona = model_to_dict(persona)
            dataafiliado = model_to_dict(afiliado)
           # datapersona.fecha_nacimiento
            datapersona.update(dataafiliado)
            kwargs["initial"] = datapersona
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            HTML(
                f'<h2><center>Datos de {persona.nombre} {persona.apellido}</center></h2>'),
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
                'familia',

            ),

            Fieldset(
                "Datos Laborales",
                HTML(
                    '<hr/>'),

                'razon_social',
                'cuit_empleador',
                'domicilio_empresa',
                'localidad_empresa',
                'fechaIngresoTrabajo',
                'rama',
                'sueldo',
                'horaJornada',
                'fechaAfiliacion',
                'categoria_laboral',
            ),

            Submit('submit', 'Volver', css_class='button white'),)