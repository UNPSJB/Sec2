# from django.shortcuts import render
from apps.afiliados.forms import AfiliadoForm, Afiliado
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


# ----------------------------- AFILIADO VIEW ----------------------------------- #

def index(request):
  template = loader.get_template('home_afiliado.html')
  return HttpResponse(template.render())
    


# class AfiliadoCreateView(CreateView):

#     model = Afiliado
#     form_class = AfiliadoForm
#     success_url = reverse_lazy('crearAfiliado')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = "Registrar Afiliado"
#         return context

#     def form_valid(self, form):
#         messages.add_message(self.request, messages.SUCCESS, 'Afiliado registrado con exito')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.add_message(self.request, messages.ERROR, form.errors)
#         return super().form_invalid(form)  


class AfiliadoCreateView(CreateView):
    model = Afiliado
    form_class = FormularioAfiliado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Alta de afiliados"
        return context
    
    
class AfliadosListView(ListView):
    model = Afiliado
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de afiliados"
        return context