from django.urls import path

from apps.reportes.views import *

app_name="reportes"


urlpatterns = [
    path('reportes/alquileres_por_mes',reportesView.as_view(), name="alquileres_por_mes"),
     path('reportes/afiliados_historico',AfiliadosReportesView.as_view(), name="afiliados_historico"),
]