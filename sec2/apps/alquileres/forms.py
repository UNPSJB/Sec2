from django import forms
from django.forms import ValidationError
from apps.personas.forms import PersonaForm,PersonaUpdateForm
from apps.personas.models import Persona
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
    encargado__persona__nombre  = forms.CharField(required=False)
    encargado__persona__apellido =forms.CharField(required=False)

# -----------------------------  SERVICIO  ----------------------------------- #
class ServiciorForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ('nombre',)
        widgets = {
           'nombre': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: Cubiertos 50'}),
            }
    

class ServicioFilterForm(FiltrosForm):
    servicio__nombre = forms.CharField(required=False)
    

# ----------------------------- SALON  ----------------------------------- #
class SalonrForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ('nombre', 'localidad', 'direccion', 'capacidad', 'encargado', 'precio','tipo_salon','servicios')
        widgets = {
           'nombre': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: PasaRatos'}),
           'direccion': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: Pedro Pascal 150'}),
           'capacidad': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 50'}),
           #'encargado': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'encargado'}),
           'precio': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),
            
       }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


class SalonFilterForm(FiltrosForm):
    salon__nombre = forms.CharField(required=False)
    salon_localidad = forms.CharField(required=False)
    salon_capacidad = forms.CharField(required=False)


# ----------------------------- ALQUILER ----------------------------------- #
class AlquilerForm(forms.ModelForm):
    #afiliado=forms.ForeignKey()
    #salon=forms.ForeignKey(Salon, related_name="alquileres", on_delete=models.CASCADE)
    #fecha_solicitud=forms.DateTimeField(auto_now_add=True, null=True, blank=True)
    #fecha_alquiler=forms.DateTimeField(null=True, blank=True) 
    #turno=forms.CharField(max_length=50, choices=turnos) #verificar bien la forma de los turnos
    #seguro=forms.DecimalField(help_text="costo del alquiler", max_digits=10, decimal_places=2)
    
    class Meta:
        model = Alquiler
        fields = ('afiliado', 'salon', 'turno', 'seguro','fecha_alquiler')
        widgets = {
          # 'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
           'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
           'seguro': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),
            
       }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class AlquilerFilterForm(FiltrosForm):
    alquiler_salon_nombre = forms.CharField(required=False)
    fecha_alquiler = forms.DateField(required=False)
    turno = forms.CharField(required=False)


# ----------------------------- PAGO ----------------------------------- #
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago_alquiler
        fields = ('forma_pago', 'alquiler')
        widgets = {
           #'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
           #'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
           #'seguro': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Eje: 1000'}),
            
       }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class AlquilerFilterForm(FiltrosForm):
    alquiler_salon_nombre = forms.CharField(required=False)
    fecha_alquiler = forms.DateField(required=False)
    turno = forms.CharField(required=False)