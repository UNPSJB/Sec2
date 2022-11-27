# from django.shortcuts import render
from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse
from datetime import datetime  

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

"""     def get_queryset(self):
        qs = Afiliado.objects.all()
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            qs = qs.filter(
                estado__startswith = self.request.GET['estado']
            )
        
        if self.request.GET.get('dni') is not None:
            print('--------------------ACACCACACA-------------------------',self.request.GET['dni'])
           # AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            qs = qs.filter(
                persona__dni__icontains = self.request.GET['dni']
            )

        print(qs)

        return qs """
    





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

def afiliado_desafiliar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    fecha = datetime.now()
    a.persona.desafiliar(a,fecha)
    a.save()
    return redirect('afiliados:afiliado_listar')


def afiliado_aceptar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    a.estado= 2
    a.save()
    return redirect('afiliados:afiliado_listar')

class afiliado_ver(UpdateView):
    model = Afiliado
   
    form_class = AfiliadoVer
    success_url = reverse_lazy('afiliados:afiliado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Ver Afiliado"
        return context
    