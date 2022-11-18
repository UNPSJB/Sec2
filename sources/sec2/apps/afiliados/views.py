# from django.shortcuts import render
from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from django.contrib import messages
from sec2.utils import ListFilterView 


# ----------------------------- AFILIADO VIEW ----------------------------------- #

def index(request):
  template = loader.get_template('home_afiliado.html')
  return HttpResponse(template.render())
    

class AfiliadoCreateView(CreateView):
    model = Afiliado
    form_class = FormularioAfiliado
    success_url = reverse_lazy('afiliados:afiliado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de afiliados"
        return context
    
    


class AfliadosListView(ListFilterView):
    model = Afiliado
    
    filter_class = AfiliadoFilterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de afiliados"
        return context





class AfiliadoUpdateView(UpdateView):
    model = Afiliado
   
    form_class = FormularioAfiliadoUpdate
    success_url = reverse_lazy('afiliados:modificarAfiliado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Afiliado"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'afiliado modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


#def desafiliar():
 #   pk=kwargs.get('pk')
  #  persona = Persona.objects.get(pk=pk)
  #  Persona.desafiliar(Persona)

class AfiliadoDeleteView(DeleteView):
    model = Afiliado
    success_url = reverse_lazy('afiliados:EliminarAfiliados')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        pk=kwargs.get('pk')
        try:
            self.object.delete() #utilizar el metodo desafiliar de persona
            messages.add_message(self.request, messages.SUCCESS, f'Afiliado dado de baja con éxito')
        finally:
            return redirect(success_url)