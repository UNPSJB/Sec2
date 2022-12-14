from cProfile import label
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django.forms import ValidationError
from .models import Afiliado
from apps.personas.forms import PersonaForm, PersonaUpdateForm
from apps.personas.models import Persona
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django.forms.models import model_to_dict
from sec2.utils import FiltrosForm


class AfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude = ['persona', 'tipo', 'estado']

        widgets = {

            'fechaIngresoTrabajo': forms.DateInput(attrs={'type': 'date'}),
            'fechaAfiliacion': forms.DateInput(attrs={'type': 'date'})
        }

        labels = {
            'fechaIngresoTrabajo': "fecha de ingreso al trabajo",
            'fechaAfiliacion': "Fecha de afiliacion"
        }


class FormularioAfiliado(forms.ModelForm):
    fechaAfiliacion = forms.DateField()

    class Meta:
        model = Persona
        fields = '__all__'
        help_texts = {
            'dni': 'Tu numero de documento sin puntos',
        }

        widgets = {


            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),


        }

        labels = {
            'fecha_nacimiento': "Fecha de nacimiento",


        }

    def clean_dni(self):
        self.persona = Persona.objects.filter(
            dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_afiliado:
            raise ValidationError("Ya existe un afiliado activo con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        print(valid)
        print(personaForm.is_valid())
        print(afiliadoForm.is_valid())
        return valid and personaForm.is_valid() and afiliadoForm.is_valid()

    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        afiliado = afiliadoForm.save(commit=False)
        self.persona.afiliar(afiliado, self.cleaned_data['fechaAfiliacion'])
        return afiliado

    def __init__(self, instance=None, *args, **kwargs):
        print(kwargs)
        super().__init__(*args, **kwargs)
        print(instance)

        self.helper = FormHelper()
        #self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            HTML(
                '<h2><center>Formulario de Afiliaci??n</center></h2>'),    
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

            Submit('submit', 'Guardar', css_class='button white'),)


FormularioAfiliado.base_fields.update(AfiliadoForm.base_fields)


##############################################

class AfiliadoUpdateForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = '__all__'
        exclude = ['persona', 'tipo','estado']

        widgets = {

            # 'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'date'}),
            # 'fechaAfiliacion': forms.DateInput(attrs={'type':'date'})
        }

        labels = {
            'fechaIngresoTrabajo': "fecha de ingreso al trabajo",
            'fechaAfiliacion': "Fecha de afiliacion"
        }


class FormularioAfiliadoUpdate(forms.Form):
    # ** SE COMENTO ESTA LINEA PARA QUE NO LO CHEQUEARA
    ##def clean_dni(self):
    ##     self.persona = Persona.objects#.filter(dni=self.cleaned_data['dni']).first()
    ##     if self.persona is not None and self.persona.es_afiliado:
    ##         raise ValidationError("Ya existe un afiliado activo con ese DNI")
    ##     return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        sv = super().is_valid()
        pv = self.personaForm.is_valid()
        av = self.afiliadoForm.is_valid()
        return sv and pv and av

    def save(self, commit=False):
        self.personaForm.save()
        return self.afiliadoForm.save()

    def __init__(self, initial = {}, instance=None, *args, **kwargs):
        print(args, kwargs)
        persona = instance.persona
        self.personaForm = PersonaUpdateForm(initial=initial, instance=instance.persona, *args, **kwargs)
        self.afiliadoForm = AfiliadoUpdateForm(initial=initial, instance=instance, *args, **kwargs)
        initial = dict(self.personaForm.initial)
        initial.update(self.afiliadoForm.initial)
        super().__init__(initial=initial, *args, **kwargs)


        self.helper = FormHelper()
        #self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            HTML(
                f'<h2><center>Modificar datos de {persona.nombre} {persona.apellido} </center></h2>'),
            Fieldset(
                "Datos Personales",

                HTML(
                    '<hr/>'),

                # 'dni',
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

            Submit('submit', 'Guardar nuevos cambios', css_class='button white'),)

FormularioAfiliadoUpdate.base_fields.update(PersonaUpdateForm.base_fields)
FormularioAfiliadoUpdate.base_fields.update(AfiliadoUpdateForm.base_fields)


class AfiliadoFilterForm(FiltrosForm):
    persona__nombre = forms.CharField(required=False)
    persona__dni = forms.CharField(required=False)
    cuit_empleador = forms.CharField(required=False)
    # Estado = forms.IntegerField(required=False)




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

    # def is_valid(self) -> bool:
    #     valid = super().is_valid()
    #     personaForm = PersonaUpdateForm(data=self.cleaned_data)
    #     afiliadoForm = AfiliadoUpdateForm(data=self.cleaned_data)
    #     print(valid)
    #     print(personaForm.is_valid())
    #     print(afiliadoForm.is_valid())
    #     return valid and personaForm.is_valid() and afiliadoForm.is_valid()

    # def save(self, commit=False):
    #     print(self.cleaned_data)
    #     if self.persona is None:
    #         personaForm = PersonaUpdateForm(data=self.cleaned_data)
    #         self.persona = personaForm.save()
    #     afiliadoForm = AfiliadoUpdateForm(data=self.cleaned_data)
    #     afiliado = afiliadoForm.save(commit=False)
    #     self.persona.afiliar(afiliado, self.cleaned_data['fechaAfiliacion'])
    #     return afiliado

    def __init__(self, instance=None, *args, **kwargs):
        print(kwargs)
        # model_to_dict(instance)

        if instance is not None:
            persona = instance.persona
            afiliado = instance.afiliado
            datapersona = model_to_dict(persona)
            dataafiliado = model_to_dict(afiliado)
            print(datapersona)
            print(dataafiliado)
           # datapersona.fecha_nacimiento
            datapersona.update(dataafiliado)
            kwargs["initial"] = datapersona
        super().__init__(*args, **kwargs)
        print(instance)

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