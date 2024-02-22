from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime

from apps.personas.forms import PersonaForm, PersonaUpdateForm  
from .models import Afiliado, Familiar
from .forms import *
from sec2.utils import ListFilterView
from django.db import transaction  # Agrega esta línea para importar el módulo transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
#CONSTANTE
from utils.constants import *
from datetime import date

# ----------------------------- AFILIADO VIEW ----------------------------------- #
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# ----------------------------- AFILIADO CREATE ----------------------------------- #
class AfiliadoCreateView(CreateView):
    model = Persona
    form_class = AfiliadoPersonaForm #utiliza un formulario unificado
    template_name = 'afiliados/afiliado_formulario.html'
    success_url = reverse_lazy('afiliados:afiliado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de Afiliación"
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        existing_person = Persona.objects.filter(dni=dni).first()
        
        if existing_person:
            messages.error(self.request, f'{ICON_ERROR} ERROR: Ya existe una persona registrada en el sistema como {existing_person.obtenerRol()} con el mismo DNI.')
            form = AfiliadoPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre= form.cleaned_data["nombre"].title(),
                apellido=form.cleaned_data["apellido"].title(),
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
                es_afiliado = True
            )
            persona.save()

            # Crear una instancia de Afiliado
            afiliado = Afiliado(
                persona=persona,
                razon_social=form.cleaned_data["razon_social"].title(),
                categoria_laboral=form.cleaned_data["categoria_laboral"].title(),
                rama=form.cleaned_data["rama"].title(),
                sueldo=form.cleaned_data["sueldo"],
                # fechaAfiliacion=form.cleaned_data["fechaAfiliacion"],
                fechaIngresoTrabajo=form.cleaned_data["fechaIngresoTrabajo"],
                cuit_empleador=form.cleaned_data["cuit_empleador"],
                localidad_empresa=form.cleaned_data["localidad_empresa"],
                domicilio_empresa=form.cleaned_data["domicilio_empresa"].title(),
                horaJornada=form.cleaned_data["horaJornada"],
                tipo = Afiliado.TIPO,
            )
            afiliado.save()
            detail_url = reverse('afiliados:afiliado_detalle', kwargs={'pk': afiliado.pk})
            messages.success(self.request, f'{ICON_CHECK} Alta de afiliado exitosa!')
            return redirect(detail_url)

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Corrija los errores marcados.')
        return super().form_invalid(form)

# ----------------------------- AFILIADO DETALLE ----------------------------------- #
class AfiliadoDetailView (DeleteView):
    model = Afiliado
    template_name = 'afiliados/afiliado_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Datos del afiliado"
        context['subtitulodetalle1'] = "Datos personales"
        context['subtitulodetalle2'] = "Datos de afiliación"
        context['tituloListado'] = "Dictados Incritos"
        return context

# ----------------------------- AFILIADO LIST ----------------------------------- #
class AfliadosListView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar')
    template_name = 'afiliados/afiliado_list.html'

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

# ----------------------------- AFILIADO LIST PENDIENTES DE ACTIVACION -------------------------- #
class AfliadosListPendienteView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar_pendiente')
    template_name = 'afiliados/afiliado_list_pendiente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Afiliados Pendientes"
        return context
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )
        return super().get_queryset()

# ----------------------------- AFILIADO LIST INACTIVO -------------------------- #
class AfliadosListActivoView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    success_url = reverse_lazy('afiliados:afiliado_listar_activos')
    template_name = 'afiliados/afiliado_list_activos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Afiliados Activos"
        return context
        
    def get_queryset(self):
        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_listar_activos.html'
            return Afiliado.objects.filter(
                estado__startswith = self.request.GET['estado']
            )
        return super().get_queryset()


# ----------------------------- AFILIADO UPDATE ----------------------------------- #
class AfiliadoUpdateView(UpdateView):
    model = Afiliado
    form_class = AfiliadoUpdateForm
    template_name = 'afiliados/afiliado_formulario.html'
    success_url = reverse_lazy('afiliados:afiliado_listar')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modicacion de Afiliación"
        return context
    
    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        existing_person = Persona.objects.filter(dni=dni).first()

        if existing_person:
            afiliado = form.save(commit=False)

            # Utiliza el formulario personalizado para validar los datos de la persona
            persona_form = PersonaUpdateForm(form.cleaned_data, instance=existing_person)

            if persona_form.is_valid():
                persona = persona_form.save(commit=False)
                # Utiliza una transacción para garantizar la integridad de los datos
                with transaction.atomic():
                    persona.save()
                    afiliado.save()

                messages.success(self.request, f'{ICON_CHECK} Modificación exitosa!')

                # Redirige al usuario al detalle del afiliado
                detail_url = reverse('afiliados:afiliado_detalle', kwargs={'pk': afiliado.pk})
                return redirect(detail_url)
            else:
                # Si el formulario de la persona no es válido, maneja los errores adecuadamente
                # Por ejemplo, podrías mostrar los errores en el formulario o tomar otra acción
                messages.error(self.request, f'{ICON_ERROR} Error en la validación de datos de la persona.')
                return self.render_to_response(self.get_context_data(form=persona_form))

        else:
            messages.error(self.request, f'{ICON_ERROR} La persona no está registrada en el sistema.')
            form = AfiliadoPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.warning(self.request, f'{ICON_TRIANGLE} Corrija los errores marcados.')
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        return super().form_invalid(form)
# ----------------------------- AFILIADO ACEPTAR ----------------------------------- #
def afiliado_aceptar(request, pk):
    afiliado = Afiliado.objects.get(pk=pk)
    # Establecer la fecha de afiliación a la fecha actual
    afiliado.fechaAfiliacion = date.today()
    afiliado.estado = 2
    afiliado.persona.es_afiliado = True
    afiliado.persona.save()
    afiliado.save()
    messages.success(request, f'{ICON_CHECK} El afiliado ha sido aceptado.')
    return redirect('afiliados:afiliado_listar')

# ----------------------------- DESAFILIAR AFILIADO -----------------------------------
def afiliado_desafiliar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    fecha = datetime.now()
    a.persona.desafiliar(a,fecha)
    a.save()
    messages.success(request, f'{ICON_CHECK} Se ha desafiliado.')
    return redirect('afiliados:afiliado_listar')

#---------- HTML PARA FUNCIONALIDADES PENDIENTES
def funcionalidad_pendiente(request):
    return render(request, 'funcionalidad_pendiente.html')

def es_menor_de_edad(self, fecha_nacimiento):
    # Verificar si la fecha de nacimiento es menor de edad (menor de 18 años)
    hoy = date.today()
    return (hoy - fecha_nacimiento).days < 365 * 18

# ----------------------------- CREACIÓN DE FAMILIAR -----------------------------
class FamiliaCreateView(CreateView):
    model = Familiar
    form_class = GrupoFamiliarPersonaForm #utiliza un formulario unificado
    template_name = 'grupoFamiliar/grupo_familiar_alta.html'
    success_url = reverse_lazy('afiliados:afiliado_crear')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Carga Familiar"
        return context
    
    def form_valid(self, form):
        dni = form.cleaned_data["dni"]

        afiliado = get_object_or_404(Afiliado, pk=self.kwargs.get('pk'))
        existing_person = Persona.objects.filter(dni=dni).first()
        if existing_person:
            messages.error(self.request, f'{ICON_ERROR} ERROR: Ya existe una persona registrada en el sistema como {existing_person.obtenerRol()} con el mismo DNI.')
            form = GrupoFamiliarPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            # Verificar si ya hay un familiar con el tipo "Esposo/a"
            esposo_existente = afiliado.familia.filter(tipo=1).exists()
            if esposo_existente and form.cleaned_data["tipo"] == '1':
                messages.error(self.request, f'{ICON_ERROR} Ya existe un esposo/a para el afiliado asociado.')
                form = GrupoFamiliarPersonaForm(self.request.POST)
                # return self.render_to_response(self.get_context_data(form=form))
                return self.form_invalid(form)

            # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
            if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self, form.cleaned_data["fecha_nacimiento"]):
                messages.error(self.request, f'{ICON_ERROR} El Hijo/a debe ser menor de edad.')
                form = GrupoFamiliarPersonaForm(self.request.POST)
                return self.form_invalid(form)
            
            persona = Persona(
                dni=dni,
                cuil=form.cleaned_data["cuil"],
                nombre= form.cleaned_data["nombre"].title(),
                apellido=form.cleaned_data["apellido"].title(),
                fecha_nacimiento=form.cleaned_data["fecha_nacimiento"],
                mail=form.cleaned_data["mail"],
                celular=form.cleaned_data["celular"],
                estado_civil=form.cleaned_data["estado_civil"],
                nacionalidad=form.cleaned_data["nacionalidad"],
                direccion=form.cleaned_data["direccion"],
                es_grupo_familiar = True
            )
            persona.save()

            # Crear una instancia de Afiliado
            familiar = Familiar(
                tipo =form.cleaned_data["tipo"],
                persona = persona
            )
            familiar.save()

            afiliado.familia.add(familiar)

            messages.success(self.request, f'{ICON_CHECK} Carga de familiar exitosa!')
            detail_url = reverse('afiliados:afiliado_detalle', kwargs={'pk': afiliado.pk})
            return redirect(detail_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
# ----------------------------- DETALLE DE FAMILIAR -----------------------------
class FamiliarDetailView(DeleteView):
    model = Familiar
    template_name = 'grupoFamiliar/grupo_familiar_detalle.html'

    def get_object(self, queryset=None):
        afiliado_pk = self.kwargs.get('pk')
        familiar_pk = self.kwargs.get('familiar_pk')
        self.afiliado = Afiliado.objects.get(pk=afiliado_pk)
        return Familiar.objects.get(afiliado__pk=afiliado_pk, pk=familiar_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        familiar = self.object
        context['titulo'] = "Datos del familiar"
        context['tituloListado'] = "Dictados Insciptos"
        context['afiliado'] = self.afiliado
        return context

class FamiliarDetailView_(DeleteView):
    model = Familiar
    template_name = 'grupoFamiliar/grupo_familiar_detalle_.html'

    def get_object(self, queryset=None):
        familiar_pk = self.kwargs.get('familiar_pk')
        return Familiar.objects.get(pk=familiar_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        familiar = self.object
        context['titulo'] = "Datos del familiar"
        context['tituloListado'] = "Dictados Insciptos"
        # Obtener el afiliado relacionado con el familiar
        afiliado = get_object_or_404(Afiliado, familia=familiar)            

        context['afiliado'] = afiliado
        return context
# ----------------------------- UPDATE DE FAMILIAR -----------------------------
class FamiliarUpdateView(UpdateView):
    model = Familiar
    form_class = GrupoFamiliarPersonaUpdateForm
    template_name = 'grupoFamiliar/grupo_familiar_editar.html'

    def get_object(self, queryset=None):
        afiliado_pk = self.kwargs.get('pk')
        familiar_pk = self.kwargs.get('familiar_pk')
        self.afiliado = Afiliado.objects.get(pk=afiliado_pk)
        return Familiar.objects.get(afiliado__pk=afiliado_pk, pk=familiar_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modicacion de Familiar"
        return context
    
    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        
        #chequeo si existe la persona
        existing_person = Persona.objects.filter(dni=dni).first()

        if existing_person:
            #si existe la persona entonces verifico que mi afiliado tenga a este familiar
            afiliado = self.afiliado
            # Verifico si el afiliado tiene al familiar
            if afiliado.familia.filter(persona=existing_person).exists():
                # El afiliado tiene al familiar

                # Obtengo el objeto Familiar asociado al afiliado y la persona existente
                familiar = get_object_or_404(Familiar, afiliado=afiliado, persona=existing_person)

                if form.cleaned_data["tipo"] == '1' and not familiar.tipo == 1:
                    # Verificar si ya hay un familiar con el tipo "Esposo/a"
                    esposo_existente = afiliado.familia.filter(tipo=1).exists()
                    if esposo_existente:
                        messages.error(self.request, f'{ICON_ERROR} Ya existe un esposo/a para el afiliado asociado.')
                        form = GrupoFamiliarPersonaForm(self.request.POST)
                        # return self.render_to_response(self.get_context_data(form=form))
                        return self.form_invalid(form)

                # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
                if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self,form.cleaned_data["fecha_nacimiento"]):
                    messages.error(self.request, f'{ICON_ERROR} El Hijo/a debe ser menor de edad.')
                    form = GrupoFamiliarPersonaForm(self.request.POST)
                    return self.form_invalid(form)
            

                familiar = form.save(commit=False)
                # Utiliza el formulario personalizado para validar los datos de la persona
                persona_form = PersonaUpdateForm(form.cleaned_data, instance=existing_person)
                if persona_form.is_valid():
                    persona = persona_form.save(commit=False)

                    # Utiliza una transacción para garantizar la integridad de los datos
                    with transaction.atomic():
                        persona.save()
                        familiar.tipo = form.cleaned_data["tipo"]
                        familiar.save()

                    messages.success(self.request, f'{ICON_CHECK} Modificación de familiar exitosa!')
                    afiliado_pk = self.kwargs.get('pk')

                    # Redirige al detalle del familiar en lugar del detalle del afiliado
                    familiar_pk = self.kwargs.get('familiar_pk')
                    familiar_detail_url = reverse('afiliados:familiar_detalle', kwargs={'pk': afiliado_pk, 'familiar_pk': familiar_pk})

                    # Agrega un pequeño script de JavaScript para cerrar la ventana y recargar la página
                    return HttpResponseRedirect(familiar_detail_url)
                else: 
                    messages.error(self.request, f'{ICON_ERROR} Error en la validación de datos de la persona.')
                    return self.render_to_response(self.get_context_data(form=persona_form))
            else:
                # El afiliado no tiene al familiar
                messages.error(self.request, f'{ICON_ERROR} El afiliado no tiene a este familiar.')
                return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.error(self.request, f'{ICON_ERROR} La persona no está registrada en el sistema.')
            form = GrupoFamiliarPersonaUpdateForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
    
# --------- SE REPITE PORQUE ES ACCEDIDO DE OTRA FORMA
class FamiliarUpdateView_(UpdateView):
    model = Familiar
    form_class = GrupoFamiliarPersonaUpdateForm
    template_name = 'grupoFamiliar/grupo_familiar_editar_.html'

    def get_object(self, queryset=None):
        familiar_pk = self.kwargs.get('familiar_pk')
        return Familiar.objects.get(pk=familiar_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modicacion de Familiar"
        familiar = self.object
        # Obtener el afiliado relacionado con el familiar
        afiliado = get_object_or_404(Afiliado, familia=familiar)            

        context['afiliado'] = afiliado
        return context
    
    def form_valid(self, form):
        dni = form.cleaned_data["dni"]
        
        #chequeo si existe la persona
        existing_person = Persona.objects.filter(dni=dni).first()

        if existing_person:
            #si existe la persona entonces verifico que mi afiliado tenga a este familiar
            familiar = self.object
            afiliado = get_object_or_404(Afiliado, familia=familiar) 
            # Verifico si el afiliado tiene al familiar
            if afiliado.familia.filter(persona=existing_person).exists():
                # El afiliado tiene al familiar

                # Obtengo el objeto Familiar asociado al afiliado y la persona existente
                familiar = get_object_or_404(Familiar, afiliado=afiliado, persona=existing_person)

                if form.cleaned_data["tipo"] == '1' and not familiar.tipo == 1:
                    # Verificar si ya hay un familiar con el tipo "Esposo/a"
                    esposo_existente = afiliado.familia.filter(tipo=1).exists()
                    if esposo_existente:
                        messages.error(self.request, f'{ICON_ERROR} Ya existe un esposo/a para el afiliado asociado.')
                        form = GrupoFamiliarPersonaForm(self.request.POST)
                        # return self.render_to_response(self.get_context_data(form=form))
                        return self.form_invalid(form)

                # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
                if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self,form.cleaned_data["fecha_nacimiento"]):
                    messages.error(self.request, f'{ICON_ERROR} El Hijo/a debe ser menor de edad.')
                    form = GrupoFamiliarPersonaForm(self.request.POST)
                    return self.form_invalid(form)
            

                familiar = form.save(commit=False)
                # Utiliza el formulario personalizado para validar los datos de la persona
                persona_form = PersonaUpdateForm(form.cleaned_data, instance=existing_person)
                if persona_form.is_valid():
                    persona = persona_form.save(commit=False)

                    # Utiliza una transacción para garantizar la integridad de los datos
                    with transaction.atomic():
                        persona.save()
                        familiar.tipo = form.cleaned_data["tipo"]
                        familiar.save()

                    messages.success(self.request, f'{ICON_CHECK} Modificación de familiar exitosa!')
                    afiliado_pk = self.kwargs.get('pk')

                    # Redirige al detalle del familiar en lugar del detalle del afiliado
                    familiar_pk = self.kwargs.get('familiar_pk')
                    familiar_detail_url = reverse('afiliados:familiar_detalle_', kwargs={'familiar_pk': familiar_pk})

                    # Agrega un pequeño script de JavaScript para cerrar la ventana y recargar la página
                    return HttpResponseRedirect(familiar_detail_url)
                else: 
                    messages.error(self.request, f'{ICON_ERROR} Error en la validación de datos de la persona.')
                    return self.render_to_response(self.get_context_data(form=persona_form))
            else:
                # El afiliado no tiene al familiar
                messages.error(self.request, f'{ICON_ERROR} El afiliado no tiene a este familiar.')
                return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.error(self.request, f'{ICON_ERROR} La persona no está registrada en el sistema.')
            form = GrupoFamiliarPersonaUpdateForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        
# ----------------------------- FAMILIAR ELIMINAR -----------------------------------
def familiar_eliminar(request, pk, familiar_pk):
    # Obtener el objeto Familiar
    familiar = get_object_or_404(Familiar, pk=familiar_pk)
    familiar.activo = False

    # print(familiar)
    # fecha = datetime.now()
    # familiar.persona.desafiliar(familiar,fecha)
    familiar.save()
    messages.success(request, f'{ICON_CHECK} Se ha desafiliado.')
    return redirect('afiliados:afiliado_listar')
