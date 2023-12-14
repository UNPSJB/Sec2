from django import forms
from apps.cursos.forms.titular_forms import *
from ..models import Dictado
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from sec2.utils import FiltrosForm
from utils.constants import *

class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = '__all__'
        # fields = ['fecha_inicio','fecha_fin', 'aula', 'precio']
        widgets ={   
            'fecha_inicio': forms.DateInput(attrs={'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date'}),
            }
        
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

class DictadoFilterForm(FiltrosForm):
    fecha_inicio  = forms.DateField(required=False)
    fecha_fin =forms.DateField(required=False)
