from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from .models import Afiliado

class FormularioAfiliado(forms.ModelForm):

    class Meta:
        model = Afiliado
        fields = '__all__'
        Widgets ={
            'fechaNacimiento': forms.DateInput(attrs={'type':'date'}),
            'fechaIngresoTrabajo': forms.DateInput(attrs={'type':'date'}),
            'fechaAfiliacion': forms.DateInput(attrs={'type':'date'})
            }