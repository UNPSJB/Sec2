from django import forms
from django.db.models import Q, Model, fields
from django.http import HttpResponse
from decimal import Decimal
from datetime import date
from django.views.generic.list import ListView
import csv
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML


class FiltrosForm(forms.Form):
    orden = forms.CharField(required=False)

    def filter(self, qs, filters):
        return qs.filter(dict_to_query(filters))  # aplicamos filtros

    def sort(self, qs, ordering):
        for o in ordering.split(','):
            if o != '':
                qs = qs.order_by(o)  # aplicamos ordenamiento
        return qs

    def apply(self, qs):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            ordering = cleaned_data.pop("orden", None)
            if len(cleaned_data) > 0:
                qs = self.filter(qs, cleaned_data)
            if ordering:
                qs = self.sort(qs, ordering)
        return qs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method="GET"
        fields = list(self.fields.keys())
        self.helper.layout = Layout(*fields,
            Submit('submit', 'Filtrar', css_class='button white'),) 

class ListFilterView(ListView):
    filter_class = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filter_class:
            context['filtros'] = self.filter_class(self.request.GET)
            context['query'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.filter_class:
            filtros = self.filter_class(self.request.GET)
            return filtros.apply(qs)
        return qs
   