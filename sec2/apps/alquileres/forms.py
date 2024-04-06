from django import forms
from django.forms import ValidationError
from apps.afiliados.models import Afiliado
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
from utils.choices import ESTADO_CIVIL, MAX_LENGTHS, NACIONALIDADES
from .models import Salon, Servicio, Alquiler, Pago_alquiler
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from sec2.utils import FiltrosForm
from utils.constants import *
from datetime import date



# ----------------------------- ENCARGADO  ----------------------------------- #
class EncargadorForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'celular', 'direccion', 'nacionalidad', 'mail', 'estado_civil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
   
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        edad = date.today().year - fecha_nacimiento.year
        if edad < 18 or edad >= 100:
            raise forms.ValidationError("Debes ser mayor de 18 años y menor de 100 años.")
        return fecha_nacimiento


class EncargadoFilterForm(FiltrosForm):
    persona__dni = forms.CharField(required=False, label="Dni" )
    persona__apellido = forms.CharField(required=False, label="Apellido")


class EncargadoUpdateForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['tipo', 'hasta', 'persona']
        labels = {
            'ejerce_desde': "Fecha desde que empezo a ejercer",
        }

    def __init__(self, *args, **kwargs):
        super(EncargadoUpdateForm, self).__init__(*args, **kwargs)
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


# -----------------------------  SERVICIO  ----------------------------------- #
class ServiciorForm(forms.ModelForm):    
    class Meta:
        model = Servicio
        fields = ('nombre',)
        widgets = {
           'nombre': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: Cubiertos 50'}),
            }
    

class ServicioFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)    

# ----------------------------- SALON  ----------------------------------- #
class SalonrForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ('nombre', 'localidad', 'direccion', 'capacidad', 'precio','tipo_salon','servicios')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: PasaRatos'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: Pedro Pascal 150'}),
            'capacidad': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 50'}),
            'tipo_salon': forms.RadioSelect(attrs={'class': 'tipo_salon-radio'}),  # Agrega la clase CSS personalizada al widget del campo de turno

            #'encargado': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'encargado'}),
            'precio': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),
            'servicios': forms.CheckboxSelectMultiple(attrs={'class': 'servicios-checkbox'}), 
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_salon'].choices = [(1, 'Polideportivo'), (2, 'Multiuso')]



class SalonFilterForm(FiltrosForm):
    salon__nombre = forms.CharField(required=False)
    salon_localidad = forms.CharField(required=False)
    salon_capacidad = forms.CharField(required=False)


# ----------------------------- ALQUILER ----------------------------------- #
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ('afiliado', 'salon', 'turno', 'seguro','fecha_alquiler')
        widgets = {
          # 'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
           'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
           'seguro': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),
            'turno': forms.RadioSelect(attrs={'class': 'turno-radio'}),  # Agrega la clase CSS personalizada al widget del campo de turno
       }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['afiliado'].queryset = Afiliado.objects.filter(estado=2)  # Filtra por estado activo (2)
        self.fields['afiliado'].label_from_instance = lambda obj: f"{obj.persona.dni} | {obj.persona.apellido} {obj.persona.nombre} | {obj.razon_social}" if obj.persona else obj.razon_social
        
        self.fields['salon'].queryset = Salon.objects.filter(fechaBaja=None)
        self.fields['salon'].label_from_instance = lambda obj: f"{obj.nombre} | Capacidad: {obj.capacidad} | ${obj.precio}"
        self.fields['turno'].choices = [('Mañana', 'Mañana'), ('Noche', 'Noche')]

        
class AlquilerFilterForm(FiltrosForm):
    alquiler_salon_nombre = forms.CharField(required=False)
    fecha_alquiler = forms.DateField(required=False)
    turno = forms.CharField(required=False)


# ----------------------------- PAGO ----------------------------------- #
class PagoForm(forms.ModelForm):
    # forma_pago = forms.ChoiceField(choices=[('total', 'Total'), ('cuota', 'Cuota')])
    alquiler = forms.ChoiceField(choices=[])
   

    class Meta:
        model = Pago_alquiler
        fields = ('forma_pago', 'alquiler')
        widgets = {
            'forma_pago': forms.RadioSelect(attrs={'class': 'turno-radio'}),  # Agrega la clase CSS personalizada al widget del campo de turno

           #'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
           #'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
           #'seguro': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),   
       }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        alquileres_sin_pagos = Pago_alquiler.alquileres_sin_pago()
        choices = [(alquiler.id, f'{alquiler.afiliado.persona.nombre} - {alquiler.salon.nombre} - {alquiler.fecha_alquiler.strftime("%d/%m/%Y")} - {alquiler.turno}') for alquiler in alquileres_sin_pagos]
        self.fields['alquiler'].choices = choices
        self.fields['forma_pago'].choices = [('total', 'Total'), ('cuota', 'Cuota')]


    def clean_alquiler(self):
        alquiler_id = self.cleaned_data['alquiler']
        try:
            alquiler = Alquiler.objects.get(pk=alquiler_id)
            return alquiler
        except Alquiler.DoesNotExist:
            raise forms.ValidationError("El alquiler seleccionado no es válido.")
        
class AlquilerFilterForm(FiltrosForm):
    alquiler_salon_nombre = forms.CharField(required=False)
    fecha_alquiler = forms.DateField(required=False)
    turno = forms.CharField(required=False)


class PagoAlquilerForm(forms.ModelForm):
    class Meta:
        model = Pago_alquiler
        fields = ['forma_pago']