from apps.personas.models import Persona, Vinculo
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, ValidationError
from django.forms import BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django_select2 import forms as s2forms


class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        #exclude=['persona', 'tipo']
        Widgets ={
            'fechaNacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
PersonaForm.base_fields.update(PersonaForm.base_fields)

class PersonaUpdateForm(ModelForm):
   
    class Meta:
        model = Persona
        # NO SE EXCLUYE EL DNI PARA QUE LO MUESTRE Y MODIFIQUE
        # exclude=['dni', "familia",'es_afiliado','es_alumno','es_profesor','es_encargado']
        exclude=["familia",'es_afiliado','es_alumno','es_profesor','es_encargado']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'guardarAfiliado'
        self.helper.layout = Layout(
            Fieldset(
                   "",
                HTML(
                    '<hr/>'),
                    'fecha_nacimiento',
                    'nombre',
                    'apellido',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'celular',      
            
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class PersonaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "dni__icontains",
        "nombre__icontains",
        "apellido__icontains",
    ]

class BuscadorPersonasForm(forms.Form):
   buscar = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=PersonaWidget)



class VinculoForm(forms.ModelForm):
    class Meta:
        model = Vinculo
        fields = '__all__'
        # fields = ("tipo",
        #           "vinculado")
        widgets = {
            'vinculado': PersonaWidget
        }

class BaseVinculoFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.template = 'bootstrap5/table_inline_formset.html'
        self.helper.add_input(Submit('submit', 'Guardar'))
    
    def clean(self):
        personas = [p['vinculado'].id for p in self.cleaned_data if 'vinculado' in p.keys()]
        if len(set(personas)) != len(personas):
            raise ValidationError("Solo puede existir un tipo de relacion con una persona")
        # Validar no tener vinculos recursivos

VinculoFormSet = modelformset_factory(Vinculo, form=VinculoForm, formset=BaseVinculoFormSet,
    extra=1,
    can_delete=True
)