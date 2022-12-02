from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

def FamiliaCreateView(request, pk):
    persona = Persona.objects.get(pk=pk)
    if request.method == 'POST':
        formset = VinculoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            vinculos = formset.save(commit=False)
            for v in vinculos:
                v.vinculante = persona
                v.save()
            for d in formset.deleted_objects:
                d.delete()
        print(formset.errors)
    formset = VinculoFormSet(queryset=persona.vinculados.all())
    return render(request, 'personas/vinculo_form.html', {
        'formset': formset, 'persona': persona})