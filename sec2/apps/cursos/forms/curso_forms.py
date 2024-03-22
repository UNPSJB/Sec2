from datetime import timezone
from django import forms
from ..models import Actividad, Curso, ListaEspera, PagoProfesor
from utils.constants import *
from utils.choices import *
from sec2.utils import FiltrosForm

#----------------------- CURSO --------------------
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        exclude= ['es_convenio', 'actividad', 'cupo', 'fechaBaja']

    area = forms.ChoiceField(
        choices=[('', '---------')] + AREAS,  # Agrega el valor por defecto a las opciones de AREAS
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre_lower = nombre.lower()  # Convertir a minúsculas

        # Exclude the current instance from the queryset (assuming instance is available in the form)
        curso_id = self.instance.id if self.instance else None

        existe_curso = Curso.objects.filter(nombre__iexact=nombre_lower).exclude(id=curso_id).exists()

        if existe_curso:
            raise forms.ValidationError('El nombre del curso ya existe. Por favor, elige otro nombre.')

        return nombre
    
    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        # self.fields['actividad'].label = 'Actividad'
        # self.fields['actividad'].queryset = Actividad.objects.all().order_by('nombre')
        tipo_curso = kwargs.get('initial', {}).get('tipo_curso')
        if tipo_curso == 'convenio':
            self.fields['area'].initial = 0
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['area'].required = False
            self.fields['costo'].initial = 0
        else:
            if tipo_curso == 'sec':
                self.fields['area'].widget = forms.Select(choices=[(0, "Capacitación"), (1, "Cultura")])
                self.fields['area'].required = True
            else:
                if tipo_curso == 'actividad':
                    self.fields['area'].initial = 2
                    self.fields['area'].widget = forms.HiddenInput()
                    self.fields['area'].required = False
                else:
                    self.fields['area'].widget = forms.Select(choices=AREAS)
                    self.fields['area'].required = True

class CursoFilterForm(FiltrosForm):
    nombre = forms.CharField(required=False)
    area = forms.ChoiceField(
        label='Área',
        choices=[('', '---------')] + list(AREAS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    actividad = forms.ModelChoiceField(
        queryset=Actividad.objects.all().order_by('nombre'),
        label='Actividad',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # duracion = forms.ChoiceField(
    #     label='Duración',
    #     choices=[('', '---------')] + list(DURACION),
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    es_convenio = forms.BooleanField(
        label='Conv. Provincial',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        try:
            return int(duracion)
        except (ValueError, TypeError):
            # Si no se puede convertir a un número, devuelve None
            return None
        

class ListaEsperaAdminForm(forms.ModelForm):
    class Meta:
        model = ListaEspera
        fields = '__all__'

    def clean_fechaInscripcion(self):
        # Devuelve la fecha y hora actual
        return timezone.now()
    



class PagoProfesorForm(forms.ModelForm):
    class Meta:
        model = PagoProfesor
        fields = '__all__'
        exclude = ['profesor', 'desde']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }