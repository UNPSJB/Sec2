from decimal import Decimal
from typing import Any
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
import json
from utils import choices , funciones
from apps.afiliados.views import redireccionar_detalle_rol
from apps.alquileres.models import Alquiler
from django.views.generic import TemplateView
from datetime import datetime
from collections import Counter, defaultdict
from django.db.models import Count

from apps.afiliados.models import Afiliado
from apps.cursos.models import Curso, DetallePagoAlumno, Dictado
from django.db.models import Count

from apps.cursos.forms.curso_forms import CursoFilterForm 
from apps.reportes.forms import CursosListFilterForm , YearcomparacionForm , YearForm
from sec2.utils import get_filtro_roles, get_selected_rol_pk
from django.db.models import Q

class AfiliadosReportesView(TemplateView):
    template_name = 'reporte_afiliados_historico.html'

    def get_graph_afiliados(self, year):
        data_dados_baja = Counter()
        data_dados_alta = Counter()
        
        afiliados_por_mes = Afiliado.objects.filter(Q(fechaAfiliacion__year=year) | Q(hasta__year=year))
        for afiliado in afiliados_por_mes:
            if afiliado.hasta:  # Confirmado
                month = afiliado.hasta.month
                cuit_empleador = afiliado.cuit_empleador
                
                data_dados_baja[month] += 1

            if afiliado.afiliado.fechaAfiliacion != None:
                    month = afiliado.fechaAfiliacion.month
                    data_dados_alta[month] += 1

        data_dados_alta_list = [data_dados_alta[month] for month in range(1, 13)]
        data_dados_baja_list = [data_dados_baja[month] for month in range(1, 13)]
        
        categories = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        return data_dados_alta_list, data_dados_baja_list , categories
    def get_armar_contexto(self, data_dados_alta_list, data_dados_baja_list, categories):
        context = dict()
        context['graph_afiliados'] = {
            'data_dados_alta_list': data_dados_alta_list,
            'data_dados_baja_list': data_dados_baja_list,
            'categories': categories,
            'y_axis_title': 'Total de alquileres',  # Y-axis title
        }
        context['filter_form'] = get_filtro_roles(self.request)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['titulo'] = 'Reportes de afiliados'
        year = datetime.today().year
        # Get the data and categories for the graph
        context  = self.get_armar_contexto(*self.get_graph_afiliados(year))
        
        context['year'] = year
        context['form_year'] = YearForm(self.request.GET) 
        context['filter_form'] = get_filtro_roles(self.request)

        return context
    
    def get(self, request, *args, **kwargs):
        filter_rol = get_filtro_roles(request)
        rol = get_selected_rol_pk(filter_rol)

        if rol is not None:
            return redireccionar_detalle_rol(rol)
        
        form = YearForm(request.GET)
        if form.is_valid():
            anio =  form.cleaned_data['year']
            if anio is not None:
                context = self.get_armar_contexto(*self.get_graph_afiliados(int(anio)))
                context['year'] = int(anio)
                context['form_year'] = form
            return render(request, 'reporte_afiliados_historico.html', context)

        return super().get(request, *args, **kwargs)
       

class reportesView(TemplateView):
    template_name = 'reporte_alquileres_por_mes.html'
    
    def get_graph_alquileres(self, anio):

        data_confirmados = Counter()
        data_enCurso = Counter()
        data_finalizados = Counter()
        data_cancelados = Counter( )

        fecha_inicio_anio = datetime(anio, 1, 1)
        fecha_fin_anio = datetime(anio, 12, 31)

        alquileres_por_mes = Alquiler.objects.filter(fecha_alquiler__gte=fecha_inicio_anio, fecha_alquiler__lte=fecha_fin_anio)
        
        # Counting rentals for each month and state
        for alquiler in alquileres_por_mes:
            month = alquiler.fecha_alquiler.month
            if alquiler.estado == 1:  # Confirmado
                data_confirmados[month] += 1
            elif alquiler.estado == 2:  # Cancelado
                data_enCurso[month] += 1
            elif alquiler.estado == 3:  # Cancelado
                data_finalizados[month] += 1
            elif alquiler.estado == 4:  # Finalizado
                data_cancelados[month] += 1

        # Converting the Counters to lists of counts for each month
        data_confirmados_list = [data_confirmados[month] for month in range(1, 13)]
        data_enCurso_list = [data_enCurso[month] for month in range(1, 13)]
        data_finalizados_list = [data_finalizados[month] for month in range(1, 13)]
        data_cancelados_list = [data_cancelados[month] for month in range(1, 13)]

        # Defining categories for X-axis
        categories = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        return data_confirmados_list, data_enCurso_list,  data_finalizados_list, data_cancelados_list, categories
    


    def get_armar_contexto(self, data_confirmados_list, data_enCurso_list,  data_finalizados_list, data_cancelados_list, categories):
        context = dict()
        context['graph_alquileres'] = {
            'data_confirmados_list': data_confirmados_list,
            'data_enCurso_list': data_enCurso_list,
            'data_finalizados_list': data_finalizados_list,
            'data_cancelados_list': data_cancelados_list,
            'categories': categories,
            'y_axis_title': 'Total de alquileres',  # Y-axis title
        }
        context['filter_form'] = get_filtro_roles(self.request)
        context['form_year'] = YearForm(self.request.GET)

        return context
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['titulo'] = 'Reportes de alquileres'
        yearActual =datetime.today().year
      
        # Get the data and categories for the graph
        context = self.get_armar_contexto(*self.get_graph_alquileres(yearActual))
        context['year'] = yearActual
        return context

    def get(self, request, *args, **kwargs):
        filter_rol = get_filtro_roles(request)
        rol = get_selected_rol_pk(filter_rol)

        if rol is not None:
            return redireccionar_detalle_rol(rol)

        form = YearForm(request.GET)
        if form.is_valid():
            anio =  form.cleaned_data['year']
            if anio is not None:
                context = self.get_armar_contexto(*self.get_graph_alquileres(int(anio)))
                context['year'] = int(anio)
            return render(request, 'reporte_alquileres_por_mes.html', context)  
                
        return super().get(request, *args, **kwargs)

class ReporteFinanzasCursosViews(TemplateView):

    template_name = "formulario_finanzas.html"
  
    def get_pagos(self, year):
        sumas_por_mes = defaultdict(Decimal)
        pagos = DetallePagoAlumno.objects.filter(dictado__fecha__year=year)
        for pago in pagos:
            mes = funciones.obtenerMes(int(pago.pago_alumno.fecha.month))
            sumas_por_mes[mes] += pago.total
        return [{'name': curso, 'data': [[curso, total]]} for curso, total in sumas_por_mes.items()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = datetime.now().year
        # Asegúrate de convertir el año a entero, ya que los parámetros GET son strings
        try:
            year = int(year)
        except ValueError:
            return JsonResponse({'error': 'Invalid year format'}, status=400)

        pagos_data = self.get_pagos(year)
        print(pagos_data)
        context['year'] = year
        context['datos'] = pagos_data
        context['filter_form'] = get_filtro_roles(self.request)
        pagos_data = self.get_pagos(year)
        print(pagos_data)
        context['year'] = year
        context['datos'] = pagos_data
        context['form'] = YearcomparacionForm(self.request.GET)
               

        return context

    def get(self, request, *args, **kwargs):
        filter_rol = get_filtro_roles(request)
        rol = get_selected_rol_pk(filter_rol)
        form = YearcomparacionForm(request.GET)
        print(form)
        if rol is not None:
            return redireccionar_detalle_rol(rol)
               

        return super().get(request, *args, **kwargs)

        

class ReporteCursosViews(TemplateView):
    template_name = 'reporte_cursos_torta.html'
    def get_curso_destacado(self, dictados):
        max_inscriptos = 0
        curso_max = None
        
        for curso in dictados:
            total_inscriptos = curso['afiliados_count'] + curso['familiares_count'] + curso['alumnos_count']
            if total_inscriptos > max_inscriptos:
                max_inscriptos = total_inscriptos
                curso_max = curso
        
        return curso_max

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = YearForm(request.GET)
        if form.is_valid():
            anio =  form.cleaned_data['year']
            if anio is not None:
               dictados = self.get_dictados_summary(anio)
               contexto = self.get_context_data()
               contexto['datos'] = dictados
               contexto['year'] = anio
               if dictados:
                    dest = self.get_curso_destacado(dictados)
                    contexto['dest'] = dest
                    contexto['historial_dest'] =  self.obtener_historial_curso_dest(dest['curso__nombre'], int(anio))
               else:
                    contexto['historial_dest'] = ""

              
               return render(request, 'reporte_cursos_torta.html', contexto)
    
   
        return super().get(request, *args, **kwargs)
    


    def get_dictados_summary(self, year):
        return list( Dictado.objects.
                    filter(fecha__year=year)
                    .values('curso__nombre')
                    .annotate(
            afiliados_count=Count('afiliados'),
            familiares_count=Count('familiares'),
            profesores_count=Count('profesores_dictados_inscriptos'),
            alumnos_count=Count('alumnos'),
 
        ).values('curso__nombre', 'afiliados_count', 'familiares_count', 'profesores_count', 'alumnos_count')
        )
    



    def obtenerCurso(self, nombre, year):
            return      list(Dictado.objects.
                        filter(fecha__year=year, curso__nombre = nombre)
                        .values('curso__nombre')
                        .annotate(
                        afiliados_count=Count('afiliados'),
                        familiares_count=Count('familiares'),
                        profesores_count=Count('profesores_dictados_inscriptos'),
                        alumnos_count=Count('alumnos'),
            
                        ).values('curso__nombre', 'afiliados_count', 'familiares_count', 'profesores_count', 'alumnos_count')
                        )
     

    def obtnerJsonHistorial(self, hist):
        series = []
        for anio, datas in hist.items():
              
              print("año: " + str(anio))
              print("data: ")
            
              if datas:
                print("entre datas")
                series_data = []
                for data in datas:
                    series_data.extend([
                        data['afiliados_count'], 
                        data['familiares_count'], 
                        data['profesores_count'], 
                        data['alumnos_count']
                    ])
                print("series data")
                print(series_data)    
                series.append({
                        'name': f'Year {anio}',
                        'data':series_data 
                    
                    })
              else:
                series.append({
                            'name': f'Year {anio}',
                            'data':[0,0,0,0]
                        
                            })

    
            # Convertir la lista de series a JSON
        return json.dumps(series)

    def obtener_historial_curso_dest(self, nombre, year):
         anio_hitorial = year
         historial = {}
         while(anio_hitorial > year-3):
            historial[anio_hitorial] = self.obtenerCurso(nombre, anio_hitorial)
            anio_hitorial -= 1
         return self.obtnerJsonHistorial(historial) 


    
    def get_context_data(self, **kwargs) :
            context = super().get_context_data(**kwargs)
       
            year = datetime.now().year

            # Asegúrate de convertir el año a entero, ya que los parámetros GET son strings
            try:
                year = int(year)
            except ValueError:
                return JsonResponse({'error': 'Invalid year format'}, status=400)
         
            dictados_data = self.get_dictados_summary(year)
            context['year'] = year
            context['datos'] = dictados_data
            
            dest = self.get_curso_destacado(dictados_data)
            context['dest'] = dest
            # context['hist_curso_dest']
            
            print("obtenido---------")

            context['historial_dest'] =  self.obtener_historial_curso_dest(dest['curso__nombre'], year)
            context['filter_form'] = get_filtro_roles(self.request)   
            context['form_year'] = YearForm(self.request.GET)  # Agrega el formulario al contexto

            return context