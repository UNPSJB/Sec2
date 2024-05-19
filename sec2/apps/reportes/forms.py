from datetime import timezone
from django import forms
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget
from apps.cursos.lookups import CursoLookup

class CursosListFilterForm(forms.Form):
    anio = forms.CharField(max_length=4, required=False)

    curso_nombre = AutoCompleteSelectField(
        lookup_class=CursoLookup,
        required=False,
        widget=AutoComboboxSelectWidget(CursoLookup, attrs={'class': 'form-control'})  # Proporcionar 'lookup_class' y 'attrs'
    )
  

    def get_query(self, request, term):
        queryset = super().get_query(request, term)
        return queryset.order_by('curso__nombre')[:5] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)