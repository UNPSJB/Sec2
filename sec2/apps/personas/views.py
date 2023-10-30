from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

"""
CLASE CREADA DE PRUEBA PORQUE NO FUNCABA EL ALTA DE GRUPO FAMILIAR
class FamiliaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    success_url = reverse_lazy('personas:crear_familiar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de Grupo Familiar"
        return context """

def FamiliaCreateView1(request, pk):
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
    formset = VinculoFormSet(queryset=persona.vinculados.all())
    return render(request, 'personas/vinculo_form.html', {
        'formset': formset, 'persona': persona})