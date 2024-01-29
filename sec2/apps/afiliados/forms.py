from .models import Afiliado
from apps.personas.models import Persona
from sec2.utils import FiltrosForm
from datetime import date
from utils.regularexpressions import *
from utils.constants import *
from django import forms
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