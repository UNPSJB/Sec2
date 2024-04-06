import datetime
from apps.afiliados.forms import Afiliado
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from apps.alquileres.models import Alquiler
from apps.cursos.models import PagoAlumno
from apps.personas.forms import PersonaForm, PersonaUpdateForm
from apps.personas.models import Rol
from utils.funciones import mensaje_advertencia, mensaje_error, mensaje_exito, registrar_fuentes  
from .models import Afiliado, Familiar, PagoCuota, RelacionFamiliar
from .forms import *
from sec2.utils import ListFilterView
from django.db import transaction  # Agrega esta línea para importar el módulo transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import FileResponse

#CONSTANTE
from utils.constants import *

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def existe_persona_activa(self, dni):
    latest_person = Rol.objects.filter(persona__dni=dni).order_by('-id').first()
    return latest_person and latest_person.hasta is None

# ----------------------------- AFILIADO CREATE ----------------------------------- #
class AfiliadoCreateView(CreateView):
    model = Persona
    form_class = AfiliadoPersonaForm #utiliza un formulario unificado
    template_name = 'afiliados/afiliado_formulario.html'
    success_url = reverse_lazy('afiliados:afiliado_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Formulario de Afiliación"
        personas = Persona.objects.all()
        context['clientes'] = personas
        return context

    def form_valid(self, form):
        dni = form.cleaned_data["dni"]

        if existe_persona_activa(self, dni):
            mensaje_error(self.request, f'{MSJ_PERSONA_EXISTE}')
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
    
            current_datetime = timezone.now()

            # Crear una instancia de Afiliado
            afiliado = Afiliado(
                persona=persona,
                razon_social=form.cleaned_data["razon_social"].title(),
                categoria_laboral=form.cleaned_data["categoria_laboral"].title(),
                rama=form.cleaned_data["rama"].title(),
                sueldo=form.cleaned_data["sueldo"],
                fechaIngresoTrabajo=form.cleaned_data["fechaIngresoTrabajo"],
                cuit_empleador=form.cleaned_data["cuit_empleador"],
                localidad_empresa=form.cleaned_data["localidad_empresa"],
                domicilio_empresa=form.cleaned_data["domicilio_empresa"].title(),
                horaJornada=form.cleaned_data["horaJornada"],
                tipo = Afiliado.TIPO,
                desde = current_datetime
            )
            afiliado.save()

            mensaje_exito(self.request, f'{MSJ_CORRECTO_ALTA_AFILIADO}')

            if 'guardar_y_recargar' in self.request.POST:
                return self.render_to_response(self.get_context_data(form=self.form_class()))   
            elif 'guardar_y_listar' in self.request.POST:
                return redirect('afiliados:afiliado_listar')
            return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_CORRECTION}')
        print("")
        print("ERRORES DEL FORMULARIO")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        print("")
        return super().form_invalid(form)

# ----------------------------- AFILIADO DETALLE ----------------------------------- #
    
def obtenerPagos(afiliado):
    #Obtengo el rol de mi afiliado
    rol = get_object_or_404(Rol, persona=afiliado.persona)
    return PagoAlumno.objects.filter(rol=rol).order_by('-fecha')

class AfiliadoDetailView (DeleteView):
    model = Afiliado
    template_name = 'afiliados/afiliado_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        afiliado = self.object  # Access the Afiliado instance

        context['titulo'] = "Datos del afiliado"
        context['subtitulodetalle1'] = "Datos personales"
        context['subtitulodetalle2'] = "Datos de afiliación"
        context['tituloListado1'] = "Dictados Incritos"
        context['tituloListado2'] = "Alquileres"
        
        context['relacion_familiar_list'] = afiliado.relacionfamiliar_set.all().order_by('familiar__persona__dni')
        context['pagos'] = obtenerPagos(afiliado)
        context['cuotas'] = PagoCuota.objects.filter(afiliado=afiliado)
        context['alquileres'] = Alquiler.objects.filter(afiliado=afiliado)
        return context

# ----------------------------- AFILIADO UPDATE ----------------------------------- #
class AfiliadoUpdateView(UpdateView):
    model = Afiliado
    form_class = AfiliadoUpdateForm
    template_name = 'afiliados/afiliado_formulario.html'
    success_url = reverse_lazy('afiliados:afiliado_listar')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editar'] = True
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

                mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')

                # Redirige al usuario al detalle del afiliado
                detail_url = reverse('afiliados:afiliado_detalle', kwargs={'pk': afiliado.pk})
                return redirect(detail_url)
            else:
                # Si el formulario de la persona no es válido, maneja los errores adecuadamente
                # Por ejemplo, podrías mostrar los errores en el formulario o tomar otra acción
                mensaje_error(self.request, f'{MSJ_ERROR_VALIDACION} ')
                return self.render_to_response(self.get_context_data(form=persona_form))

        else:
            mensaje_error(self.request, f'{MSJ_PERSONA_NO_EXISTE} ')
            form = AfiliadoPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        mensaje_advertencia(self.request, f'{MSJ_CORRECTION}')
        print("")
        for field, errors in form.errors.items():
            print(f"Campo: {field}, Errores: {', '.join(errors)}")
        print("")
        return super().form_invalid(form)

# ----------------------------- AFILIADO LISTADO ----------------------------------- #
class AfliadosListView(ListFilterView):
    model = Afiliado
    filter_class = AfiliadoFilterForm
    template_name = 'afiliados/afiliado_list.html'
    paginate_by = MAXIMO_PAGINATOR
    success_url = reverse_lazy('afiliados:afiliado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de afiliados"
        return context
        
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('estado') is not None:
            AfliadosListView.template_name = 'afiliado_list_aceptar.html'
            queryset = Afiliado.objects.filter(
                estado__startswith=self.request.GET['estado']
            )

        # Apply additional filters from the form
        form = AfiliadoFilterForm(self.request.GET)
        if form.is_valid():
            persona_dni = form.cleaned_data.get('persona__dni')
            persona_nombre = form.cleaned_data.get('persona__nombre')
            cuit_empleador = form.cleaned_data.get('cuit_empleador')
            estado = form.cleaned_data.get('estado')

            if persona_dni:
                queryset = queryset.filter(persona__dni=persona_dni)
            if persona_nombre:
                queryset = queryset.filter(persona__nombre__icontains=persona_nombre)
            if cuit_empleador:
                queryset = queryset.filter(cuit_empleador=cuit_empleador)
            if estado:
                queryset = queryset.filter(estado=estado)
        return queryset

# ----------------------------- AFILIADO ACEPTAR ----------------------------------- #
def afiliado_afiliar_desafiliar(request, pk, accion, origen):
    afiliado = get_object_or_404(Afiliado, pk=pk)

    if accion == 'afiliar':
        afiliado.afiliar()
        mensaje_exito(request, f'{MSJ_AFILIADO_AFILIADO} ')
    elif accion == 'desafiliar':
        afiliado.desafiliar()
        mensaje_exito(request, f'{MSJ_AFILIADO_DESAFILIADO}')

    if origen == 'listadoAfiliado':
        return redirect('afiliados:afiliado_listar')
    elif origen == 'detalleAfiliado':
        return redirect('afiliados:afiliado_detalle', pk=afiliado.pk)
#------------------------------------------------------------------------------------------
from io import BytesIO
import io
from reportlab.pdfgen import canvas

def confeccionarNota(request, pk):
    afiliado = get_object_or_404(Afiliado, pk=pk)
    buffer = generate_pdf(afiliado)
    return FileResponse(buffer, as_attachment=True, filename="nota_detalle_afiliado.pdf")

def generate_pdf(afiliado):

    registrar_fuentes()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    # locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')

    establecer_fuente_titulo(pdf)
    agregar_cabecera(pdf, afiliado)

    if afiliado.familia.exists():
        familiares = afiliado.familia.all()
        agregar_detalle(pdf, 'FAMILIARES:', 545, familiares, afiliado)

    agregar_pie_de_pagina(pdf)
    agregar_firma_y_aclaracion(pdf)
    # locale.setlocale(locale.LC_TIME, '')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer


def establecer_fuente_titulo(pdf):
    pdf.setFont('Times-Bold', 14)
    pdf.drawCentredString(300, 770, "Sindicato de Empleado de Comercio 2")
    pdf.drawCentredString(300, 745, "Acuse de afiliación")

def agregar_linea(pdf, y_position):
    pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    pdf.line(100, y_position, 520, y_position)
    pdf.setStrokeColorRGB(0, 0, 0)

def agregar_cabecera(pdf, afiliado):
    agregar_linea(pdf, 715)
    pdf.setFont("Calibri", 11)
    pdf.drawRightString(295, 695, f'DNI:')
    pdf.drawRightString(295, 675, f'Nombre:')
    pdf.drawRightString(295, 655, f'Fecha de nacimiento:')
    pdf.drawRightString(295, 635, f'Estado Civil:')
    pdf.drawRightString(295, 615, f'Razon social:')    
    pdf.drawRightString(295, 595, f'Categoría laboral:')
    pdf.drawRightString(295, 575, f'Sueldo:')
    pdf.drawRightString(295, 555, f'Cantidad a descontar:')
    pdf.drawString(300, 695, f'{afiliado.persona.dni}')
    pdf.drawString(300, 675, f'{afiliado.persona.nombre} {afiliado.persona.apellido}')
    pdf.drawString(300, 655, f'{afiliado.persona.fecha_nacimiento.strftime("%Y-%m-%d")}')
    pdf.drawString(300, 635, f'{afiliado.persona.estado_civil}')
    pdf.drawString(300, 615, f'{afiliado.razon_social}')
    pdf.drawString(300, 595, f'{afiliado.categoria_laboral}')
    pdf.drawString(300, 575, f'${afiliado.sueldo}')
    pdf.drawString(300, 555, f'${afiliado.valorCuota()}')

def agregar_detalle(pdf, titulo, y_position, familiares, afiliado):
    agregar_linea(pdf, y_position)

    pdf.setFont("Times-Italic", 11)
    pdf.drawCentredString(300, y_position - 20, titulo)
    pdf.setFont("Calibri", 11)
    
    for idx, familiar in enumerate(familiares):
        relacion = RelacionFamiliar.objects.get(afiliado=afiliado, familiar=familiar)
        tipo_relacion = relacion.get_tipo_relacion_display()
        # Detalle del familiar
        pdf.drawRightString(295, y_position - 40 - (idx * 20), f'Tipo de Relación:')
        pdf.drawRightString(295, y_position - 60 - (idx * 20), f'Dni:')
        pdf.drawRightString(295, y_position - 80 - (idx * 20), f'Nombre:')

        pdf.drawString(300, y_position - 40 - (idx * 20), f'{tipo_relacion}')
        pdf.drawString(300, y_position - 60 - (idx * 20), f'{familiar.persona.dni}')
        pdf.drawString(300, y_position - 80 - (idx * 20), f'{familiar.persona.nombre} {familiar.persona.apellido}')

def agregar_pie_de_pagina(pdf):
    pdf.setFont("Calibri", 11)
    pdf.drawCentredString(300, 50, 'Sec2@gmail.com')

def agregar_firma_y_aclaracion(pdf):
    pdf.setFont("Times-Bold", 10)

    # Firma
    pdf.drawRightString(200, 105, 'Firma:')
    pdf.line(200, 95, 350, 95) 

    # Aclaración
    pdf.drawRightString(200, 85, 'Nombre:')
    pdf.line(200, 75, 350, 75)  # Línea para la aclaración



def es_menor_de_edad(self, fecha_nacimiento):
    # Verificar si la fecha de nacimiento corresponde a una persona menor de 40 años
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad <= 40

def alta_familiar(request):
    if request.method == 'POST':
        form = AfiliadoSelectForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]

            if existe_persona_activa(request, dni):
                mensaje_error(request, f'{MSJ_PERSONA_EXISTE}')
                form = AfiliadoSelectForm(request.POST)

            else:
                afiliado_seleccionado_id = request.POST.get('enc_cliente')
                afiliado = get_object_or_404(Afiliado, pk=afiliado_seleccionado_id)

                if afiliado.tiene_esposo() and form.cleaned_data["tipo"] == '1':
                    mensaje_error(request, f'{MSJ_FAMILIAR_ESPOSA_EXISTE}')
                    form = AfiliadoSelectForm(request.POST)
                else:
                    if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(request,form.cleaned_data["fecha_nacimiento"]):
                        mensaje_error(request, f'{MSJ_HIJO_MAYOR_EDAD}')
                        form = AfiliadoSelectForm(request.POST)
                        context = {
                            'form': form,
                            'clientes': Afiliado.objects.filter(estado__in=[1, 2]),
                            'titulo': 'Alta de Familiar',  # Replace with your desired title
                        }
                        return render(request, 'grupoFamiliar/grupo_familiar_alta_directa.html', context)

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
                            es_grupo_familiar = True
                        )
                        persona.save()
                        
                        activo = True if afiliado.estado == 2 else False
                        familiar = Familiar(
                            persona=persona,
                            activo=activo,
                            tipo=Familiar.TIPO,
                            desde = timezone.now()
                        )
                        familiar.save()

                        relacion = RelacionFamiliar(
                            afiliado = afiliado,
                            familiar = familiar,
                            tipo_relacion =form.cleaned_data["tipo"],
                        )
                        relacion.save()
                        
                        mensaje_exito(request, f'{MSJ_FAMILIAR_CARGA_CORRECTA}')

                        form = AfiliadoSelectForm(request.POST)
                        context = {
                        'form': form,
                        'clientes': Afiliado.objects.filter(estado__in=[1, 2]),
                        'titulo': 'Alta de Familiar',  # Replace with your desired title
                        }

                        if 'guardar_y_recargar' in request.POST:
                            return render(request, 'grupoFamiliar/grupo_familiar_alta_directa.html', context)
                        elif 'guardar_y_listar' in request.POST:
                            return redirect('afiliados:grupo_familiar_listar')
                        return render(request, 'grupoFamiliar/grupo_familiar_alta_directa.html', context)

    else:
        afiliados_pendientes_activos = Afiliado.objects.filter(estado__in=[1, 2])
        form = AfiliadoSelectForm()

    context = {
        'form': form,
        'clientes': Afiliado.objects.filter(estado__in=[1, 2]),
        'titulo': 'Alta de Familiar',  # Replace with your desired title
    }
    return render(request, 'grupoFamiliar/grupo_familiar_alta_directa.html', context)


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
        existing_person = Rol.objects.filter(persona__dni=dni).first()
        
        # Si existe la persona y no tiene fecha hasta (esta activa)
        if existing_person and existing_person.hasta is None:
            mensaje_error(self.request, f'{MSJ_PERSONA_EXISTE}')
            form = GrupoFamiliarPersonaForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            if afiliado.tiene_esposo() and form.cleaned_data["tipo"] == '1':
                mensaje_error(self.request, f'{MSJ_FAMILIAR_ESPOSA_EXISTE}')
                form = GrupoFamiliarPersonaForm(self.request.POST)
                # return self.render_to_response(self.get_context_data(form=form))
                return self.form_invalid(form)

            # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
            if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self, form.cleaned_data["fecha_nacimiento"]):
                mensaje_error(self.request, f'{MSJ_HIJO_MAYOR_EDAD}')
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

            activo = True if afiliado.estado == 2 else False
            familiar = Familiar(
                persona=persona,
                activo=activo,
                tipo=Familiar.TIPO,
                desde = timezone.now()

            )
            familiar.save()
            
            relacion = RelacionFamiliar(
                afiliado = afiliado,
                familiar = familiar,
                tipo_relacion =form.cleaned_data["tipo"],
            )
            relacion.save()
            mensaje_exito(self.request, f'{MSJ_FAMILIAR_CARGA_CORRECTA}')
            detail_url = reverse('afiliados:afiliado_detalle', kwargs={'pk': afiliado.pk})
            return redirect(detail_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
# ----------------------------- DETALLE DE FAMILIAR -----------------------------
class FamiliarDetailView(DeleteView):
    model = Familiar
    template_name = 'grupoFamiliar/grupo_familiar_detalle_afiliado.html'

    def get_object(self, queryset=None):
        afiliado_pk = self.kwargs.get('pk')
        familiar_pk = self.kwargs.get('familiar_pk')
        self.afiliado = Afiliado.objects.get(pk=afiliado_pk)
        return Familiar.objects.get(afiliado__pk=afiliado_pk, pk=familiar_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ventana = self.kwargs.get('ventana')
        context['nueva_ventana'] = ventana == 'nueva_ventana'
        familiar = self.object
        context['titulo'] = "Datos del familiar"
        context['tituloListado'] = "Dictados Inscritos"
        context['afiliado'] = self.afiliado
        context['familiar'] = familiar  # Agregar el objeto familiar al contexto
        return context




class FamiliarDetailVentanaNuevaView_(DeleteView):
    model = Familiar
    template_name = 'grupoFamiliar/grupo_familiar_detalle_nueva_ventana.html'

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
        ventana = self.kwargs.get('ventana')
        context['nueva_ventana'] = ventana == 'nueva_ventana'
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

                # if form.cleaned_data["tipo"] == '1' and not familiar.tipo == 1:
                    # Verificar si ya hay un familiar con el tipo "Esposo/a"
                    # esposo_existente = afiliado.familia.filter(tipo=1).exists()
                    # if esposo_existente:
                        # mensaje_error(self.request, f'{MSJ_FAMILIAR_ESPOSA_EXISTE}')
                        # form = GrupoFamiliarPersonaForm(self.request.POST)
                        # return self.render_to_response(self.get_context_data(form=form))
                        # return self.form_invalid(form)

                # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
                # if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self,form.cleaned_data["fecha_nacimiento"]):
                    # mensaje_error(self.request, f'{MSJ_HIJO_MAYOR_EDAD}')
                    # form = GrupoFamiliarPersonaForm(self.request.POST)
                    # return self.form_invalid(form)

                familiar = form.save(commit=False)
                # Utiliza el formulario personalizado para validar los datos de la persona
                persona_form = PersonaUpdateForm(form.cleaned_data, instance=existing_person)
                if persona_form.is_valid():
                    persona = persona_form.save(commit=False)

                    # Utiliza una transacción para garantizar la integridad de los datos
                    with transaction.atomic():
                        persona.save()
                        # familiar.tipo = form.cleaned_data["tipo"]

                        familiar.save()

                    mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
                    afiliado_pk = self.kwargs.get('pk')

                    # Redirige al detalle del familiar en lugar del detalle del afiliado
                    familiar_pk = self.kwargs.get('familiar_pk')
                    familiar_detail_url = reverse('afiliados:familiar_detalle', kwargs={'pk': afiliado_pk, 'familiar_pk': familiar_pk, 'ventana':'misma_ventana'})

                    # Agrega un pequeño script de JavaScript para cerrar la ventana y recargar la página
                    return HttpResponseRedirect(familiar_detail_url)
                else: 
                    mensaje_error(self.request, f'{MSJ_ERROR_VALIDACION}')
                    return self.render_to_response(self.get_context_data(form=persona_form))
            else:
                # El afiliado no tiene al familiar
                mensaje_error(self.request, f'{MSJ_AFILIADO_NO_FAMILIAR}')
                return self.render_to_response(self.get_context_data(form=form))
        else:
            mensaje_error(self.request, f'{MSJ_PERSONA_NO_EXISTE}')
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
                        mensaje_error(self.request, f'{MSJ_FAMILIAR_ESPOSA_EXISTE}')
                        form = GrupoFamiliarPersonaForm(self.request.POST)
                        # return self.render_to_response(self.get_context_data(form=form))
                        return self.form_invalid(form)

                # Verificar si es menor de edad cuando el tipo es 'Hijo/a'
                if form.cleaned_data["tipo"] == '2' and not es_menor_de_edad(self,form.cleaned_data["fecha_nacimiento"]):
                    mensaje_error(self.request, f'{MSJ_HIJO_MAYOR_EDAD}')
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

                    mensaje_exito(self.request, f'{MSJ_EXITO_MODIFICACION}')
                    afiliado_pk = self.kwargs.get('pk')

                    # Redirige al detalle del familiar en lugar del detalle del afiliado
                    familiar_pk = self.kwargs.get('familiar_pk')
                    familiar_detail_url = reverse('afiliados:familiar_detalle_', kwargs={'familiar_pk': familiar_pk})

                    # Agrega un pequeño script de JavaScript para cerrar la ventana y recargar la página
                    return HttpResponseRedirect(familiar_detail_url)
                else: 
                    mensaje_error(self.request, f'{MSJ_ERROR_VALIDACION}')
                    return self.render_to_response(self.get_context_data(form=persona_form))
            else:
                # El afiliado no tiene al familiar
                # mensaje_error(self.request, f'{MSJ_AFILIADO_NO_FAMILIAR}')
                return self.render_to_response(self.get_context_data(form=form))
        else:
            mensaje_error(self.request, f'{MSJ_PERSONA_NO_EXISTE}')
            form = GrupoFamiliarPersonaUpdateForm(self.request.POST)
            return self.render_to_response(self.get_context_data(form=form))
        
# -----------------------------  LIST ----------------------------------- #
class RelacionFamiliarListView(ListFilterView):
    model = RelacionFamiliar
    filter_class = RelacionFamiliarFilterForm
    template_name = 'relacion_familiar_listar.html'
    paginate_by = MAXIMO_PAGINATOR
    success_url = reverse_lazy('afiliados:afiliado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Grupo Familiar"
        return context
        
    def get_queryset(self):
        queryset = super().get_queryset()

        familiar_dni = self.request.GET.get('familiar__persona__dni')
        afiliado_dni = self.request.GET.get('afiliado__persona__dni')
        tipo_relacion = self.request.GET.get('tipo_relacion')

        if familiar_dni:
            queryset = queryset.filter(familiar__persona__dni=familiar_dni)

        if afiliado_dni:
            queryset = queryset.filter(afiliado__persona__dni=afiliado_dni)

        if tipo_relacion:
            queryset = queryset.filter(tipo_relacion=tipo_relacion)

        return queryset

# ----------------------------- FAMILIAR ELIMINAR -----------------------------------
def familiar_eliminar(request, pk, familiar_pk):
    # Obtener el objeto Familiar
    familiar = get_object_or_404(Familiar, pk=familiar_pk)
    familiar.activo = False
    familiar.save()
    mensaje_advertencia(request, f'{MSJ_FAMILIAR_ELIMINADO}')
    return redirect('afiliados:afiliado_listar')

from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Q

class PagoCuotaCreateView(CreateView):
    model = PagoCuota
    form_class = PagoCuotaForm
    template_name = 'pago/pago_cuota_sindical.html'
    success_url = reverse_lazy('afiliados:pagar_cuota_sindical')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtrar roles sin fecha de finalización
        roles_sin_fecha_hasta = Rol.objects.filter(hasta__isnull=True)
        
        # Obtener personas asociadas a los roles sin fecha de finalización
        personas = Persona.objects.filter(roles__in=roles_sin_fecha_hasta)
        
        # Obtener afiliados asociados a las personas obtenidas
        afiliados = Afiliado.objects.filter(persona__in=personas)
        
        # Obtener todos los cuit_empleador únicos de los afiliados con sus respectivas razones sociales
        empleadores = Afiliado.objects.filter(
            Q(estado=1) | Q(estado=2) | Q(estado=5),  # Filtrar por estados 1 o 2
            cuit_empleador__isnull=False
        ).values('cuit_empleador', 'razon_social').distinct()

        context['titulo'] = "Cuota Sindical"
        context['afiliados'] = afiliados
        context['empleadores'] = empleadores
        return context
    
    def form_valid(self, form):
        afiliado_id = self.request.POST.get('enc_afiliado')
        cuit_empleador = self.request.POST.get('enc_cuit')
        pdf = self.request.POST.get('pdf_transferencia')
        
        if afiliado_id == '0' or cuit_empleador == '0':
            mensaje_advertencia(self.request, f'Seleccione la empresa y al afiliado')
            return super().form_invalid(form)

        afiliado = get_object_or_404(Afiliado, pk=afiliado_id)

        if afiliado.cuit_empleador != cuit_empleador:
            mensaje_error(self.request, f'{MSJ_CUIT_INVALIDO}')
            return super().form_invalid(form)

        existe_cuotas = PagoCuota.objects.filter(afiliado=afiliado).exists()

        if not existe_cuotas:
            form.instance.afiliado_id = afiliado_id
            form.instance.pdf_transferencia = pdf
            form.save()

            if afiliado.estado == 1:
                afiliado.afiliar()
                afiliado.save()
                mensaje_exito(self.request, f'{MSJ_CORRECTO_PAGO_REALIZADO} y {MSJ_CORRECTO_ALTA_AFILIADO}')
                return super().form_valid(form)

            else:
                mensaje_exito(self.request, f'{MSJ_CORRECTO_PAGO_REALIZADO}')
            
            if 'guardar_y_recargar' in self.request.POST:
                return self.render_to_response(self.get_context_data(form=self.form_class()))   
            elif 'guardar_y_listar' in self.request.POST:
                return redirect('afiliados:pago_cuota_listado')

        else:
            # Si ya existen cuotas obtengo mi ultima cuota por fecha de pago
            ultima_cuota = PagoCuota.objects.filter(afiliado=afiliado).latest('fecha_pago')
            fecha_pago = form.instance.fecha_pago
            fecha_pago_un_mes_atras = fecha_pago - relativedelta(months=1)

            if fecha_pago_un_mes_atras.month == ultima_cuota.fecha_pago.month:
                form.instance.afiliado_id = afiliado_id
                form.instance.pdf_transferencia = pdf
                form.save()
                mensaje_exito(self.request, f'{MSJ_CORRECTO_PAGO_REALIZADO}')
                return super().form_valid(form)
            else:
                mensaje_advertencia(self.request, 'El mes anterior esta sin pagar.')
                return super().form_invalid(form)




    def form_invalid(self, form):
        mensaje_advertencia(self.request, MSJ_CORRECTION)
        print("")
        print("ERRORES DEL FORMULARIO")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        print("")
        return super().form_invalid(form)

class PagoCuotaListView(ListFilterView):
    model = PagoCuota
    filter_class = PagoCuotarFilterForm
    template_name = 'pago/pago_cuota_listado.html'
    paginate_by = MAXIMO_PAGINATOR
    success_url = reverse_lazy('afiliados:afiliado_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Pago de Cuota"
        return context
        
    def get_queryset(self):
        queryset = super().get_queryset()
        afiliado_dni = self.request.GET.get('afiliado__persona__dni')
        cuit_empleador = self.request.GET.get('afiliado__cuit_empleador')  # Add this line

        if afiliado_dni:
            queryset = queryset.filter(afiliado__persona__dni=afiliado_dni)

        if cuit_empleador:
            # Use Q objects to perform OR filtering on afiliado__cuit_empleador and familiar__cuit_empleador
            queryset = queryset.filter(Q(afiliado__cuit_empleador=cuit_empleador))
        
        return queryset
    
def cuota_sindical_actualizar_estado(request):
    # Obtener todos los afiliados que están vinculados a través de sus cuotas
    afiliados_vinculados = Afiliado.objects.filter(pagos_cuotas__isnull=False).distinct()

    # Fecha actual y fecha dos meses atrás
    fecha_actual = datetime.now().date()
    fecha_dos_meses_atras = fecha_actual - relativedelta(months=2)

    for afiliado in afiliados_vinculados:
        ultima_cuota = PagoCuota.objects.filter(afiliado=afiliado).latest('fecha_pago')
        if ultima_cuota.fecha_pago < fecha_dos_meses_atras:
            if afiliado.estado == 2:
                #se lo marca como Moroso
                afiliado.estado = 5
        else:
            if afiliado.estado == 5:
                #se vuelve a marcar como activo
                afiliado.estado = 2
        
        afiliado.save()
    
    mensaje_exito(request, f'Estados de los afiliados actualizados')
    return redirect('afiliados:pago_cuota_listado')

