from django.urls import path
from .views import *
from . import views

app_name="alquiler"


urlpatterns = [
    path('',index, name="index"),
##--------------- SALON--------------------------------
    path('crear/',SalonCreateView.as_view(), name="salon_crear"),
    path('salon/<int:pk>',SalonDetailView.as_view(), name="Salon"),
    path('modificar/<int:pk>', SalonUpdateView.as_view(), name="salon_actualizar"),
#    path('mostrar/',SalonesListView.as_view(), name="salon_listar"),


##--------------- ALQUILER--------------------------------
   
   # path('crear/',AlquilerCreateView.as_view(), name="alquiler_crear"),
    #path('alquiler/<int:pk>',AlquilerDetailView.as_view(), name="Alquiler"),
    #path('modificar/<int:pk>', AlquilerUpdateView.as_view(), name="alquiler_actualizar"),
    #path('mostrar/',AlquilieresListView.as_view(), name="alquiler_listar"),
    #path('mostrar/pendientes',AlquileresListPendienteView.as_view(), name="alquiler_listar_pendiente"),
    #path('mostrar/activos',AlquileresListActivoView.as_view(), name="alquiler_listar_activos"),

##--------------- PAGO DE ALQUILER--------------------------------
   # path('crear/',PagoAlquilerCreateView.as_view(), name="pagar_alquiler_crear"),
   # path('alquiler/<int:pk>',PagoAlquilerDetailView.as_view(), name="Pago_alquiler"),
  #  path('modificar/<int:pk>', PagoAlquilerUpdateView.as_view(), name="pago_alquiler_actualizar"),
  #  path('mostrar/',PagosAlquilieresListView.as_view(), name="pago_alquiler_listar"),
]