from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Create your views here.



def FamiliaCreateView(request, pk):
    persona = Persona.objects.get(pk=pk)
    familiares = list([{'tipo': f.tipo, 'familiar': f.familiar_de} for f in persona.familiares.all()])
    if request.method == 'POST':
        formset = FamiliarFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for f in formset.forms:
                print(f)
    else:
        formset = FamiliarFormSet(initial=familiares)
    return render(request, 'personas/familiar_form.html', {
        'formset': formset, 'persona': persona})
