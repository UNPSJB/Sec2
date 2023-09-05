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
from django.views.generic.edit import CreateView
from .models import MiModelo

# ----------------------------- AFILIADO VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home_afiliado.html')
    return HttpResponse(template.render())

# class MiModeloCreateView(CreateView):
#     model = MiModelo  # Especifica el modelo con el que trabajarás
#     template_name = 'templates/afiliado_form.html'  # Especifica la plantilla HTML para el formulario
#     # fields = ['campo1', 'campo2', 'campo3']  # Especifica los campos del modelo que se mostrarán en el formulario
#     fields = ['campo1']  # Especifica los campos del modelo que se mostrarán en el formulario

#     # Opcional: Si deseas personalizar el comportamiento después de que el objeto se haya creado con éxito
#     def form_valid(self, form):
#         # Personaliza el comportamiento después de que el formulario sea válido
#         # Por ejemplo, puedes realizar acciones adicionales antes o después de guardar el objeto
#         return super().form_valid(form)

#     # Opcional: Si deseas redirigir a una página diferente después de que el objeto se haya creado con éxito
#     def get_success_url(self):
#         return reverse_lazy('afiliados:afiliado_crear')  # Reemplaza 'nombre_de_la_vista' con el nombre de la vista a la que deseas redirigir

#     # Otras personalizaciones según tus necesidades


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
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )

        return super().get_queryset()




class AfiliadoUpdateView(UpdateView):
    model = Afiliado
    form_class = FormularioAfiliadoUpdate
    success_url = reverse_lazy('afiliados:afiliado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Afiliado"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'afiliado modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        print(form.non_field_errors())
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

def afiliado_ver1(request, pk):
    template = loader.get_template('afiliado_historial.html')
    return HttpResponse(template.render())

class afiliado_ver(UpdateView):
    model = Afiliado
    form_class = FormularioAfiliadoUpdate
    success_url = reverse_lazy('afiliados:Afiliado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Afiliado"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'afiliado modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        print(form.non_field_errors())
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class AfiliadoVer():
    
    fechaAfiliacion = forms.DateField()

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['familia']
        widgets = {
            # 'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
        }

        labels = {
            'fecha_nacimiento': "Fecha de nacimiento",
        }

    def __init__(self, instance=None, *args, **kwargs):
        print(kwargs)
        # model_to_dict(instance)

        if instance is not None:
            persona = instance.persona
            afiliado = instance.afiliado
            datapersona = model_to_dict(persona)
            dataafiliado = model_to_dict(afiliado)
            print(datapersona)
            print(dataafiliado)
           # datapersona.fecha_nacimiento
            datapersona.update(dataafiliado)
            kwargs["initial"] = datapersona
        super().__init__(*args, **kwargs)
        print(instance)

        self.helper = FormHelper()
        #self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            HTML(
                f'<h2><center>Datos de {persona.nombre} {persona.apellido}</center></h2>'),
            Fieldset(
                "Datos Personales",

                HTML(
                    '<hr/>'),
                'dni',
                'nombre',
                'apellido',
                'fecha_nacimiento',
                'direccion',
                'mail',
                'nacionalidad',
                'estado_civil',
                'cuil',
                'celular',
                'familia',

            ),

            Fieldset(
                "Datos Laborales",
                HTML(
                    '<hr/>'),

                'razon_social',
                'cuit_empleador',
                'domicilio_empresa',
                'localidad_empresa',
                'fechaIngresoTrabajo',
                'rama',
                'sueldo',
                'horaJornada',
                'fechaAfiliacion',
                'categoria_laboral',
            ),

            Submit('submit', 'Volver', css_class='button white'),)

class AfiliadoDetailView (DeleteView):
    model = Afiliado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Afiliado"
        return context