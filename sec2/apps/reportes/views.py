from django.shortcuts import render

from apps.alquileres.models import Alquiler
from django.views.generic import TemplateView
from datetime import datetime
from collections import Counter
from django.db.models import Count

class reportesView(TemplateView):
    template_name = 'reporte_alquileres_por_mes.html'
    
    def get_graph_alquileres(self):
        alquileres = Alquiler.objects.all()
        print("alquileres", alquileres)

        data = Counter()
        year = datetime.now().year
        
        # Fetching counts of rentals for each month
        alquileres_por_mes = Alquiler.objects.all()
        
        # Counting rentals for each month
        for alquiler in alquileres_por_mes:
            month = alquiler.fecha_alquiler.month
            data[month] += 1
            
        # Converting the Counter to a list of counts for each month
        data_list = [data[month] for month in range(1, 13)]
        print("data_list", data_list)
            
            # Defining categories for X-axis
        categories = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        return data_list, categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reportes de alquileres'
        
        # Obtiene los datos y las categorías del gráfico
        data_list, categories = self.get_graph_alquileres()
        
        # Agrega los datos y las categorías al contexto
        context['graph_alquileres'] = {
            'data_list': data_list,
            'categories': categories,
            'y_axis_title': '1000 metric tons (MT)'  # Título del eje Y
        }
        return context
        
