from django.urls import path
from .views import *
from . import views

app_name="alquiler"


urlpatterns = [
    path('',index, name="index"),
    
    # ENCARGADO
    path('encargados/listado',EncargadoListView.as_view(), name="encargado_listar"),
    path('encargados/encargado/crear/',EncargadoCreateView.as_view(), name="encargado_alta"),
    path('encargados/encargado/<int:pk>', EncargadoDetailView.as_view(), name="encargado_detalle"),
    path('encargados/encargado/<int:pk>/editar', EncargadoUpdateView.as_view(), name="encargado_editar"),

    #SERVICIO
    path('servicios/', GestionServicioView.as_view(), name="gestion_servicio"),
    path('servicio/servicio/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detalle'),
    # path('servicios/serviio/crearServicio/',ServicioCreateView.as_view(), name="servicio_crear"),
    path('aulas/aula/<int:pk>/editar', ServicioUpdateView.as_view(), name="servicio_editar"),

##--------------- SALON--------------------------------
    path('salones/listado',SalonesListView.as_view(), name="salon_listar"),
    path('crear/',SalonCreateView.as_view(), name="salon_crear"),

    path('salon/<int:pk>',SalonDetailView.as_view(), name="Salon_detalle"),
    path('modificar/<int:pk>', SalonUpdateView.as_view(), name="salon_actualizar"),


##--------------- ALQUILER--------------------------------
   
    path('crearAlquiler/',AlquilerCreateView.as_view(), name="alquiler_crear"),
    path('alquiler/<int:pk>',AlquilerDetailView.as_view(), name="Alquiler"),
    #path('modificar/<int:pk>', AlquilerUpdateView.as_view(), name="alquiler_actualizar"),
    path('mostrarAlquileres/',AlquilieresListView.as_view(), name="alquiler_listar"),
    #path('mostrar/pendientes',AlquileresListPendienteView.as_view(), name="alquiler_listar_pendiente"),
    #path('mostrar/activos',AlquileresListActivoView.as_view(), name="alquiler_listar_activos"),

##--------------- PAGO DE ALQUILER--------------------------------
    path('crearPago/',PagoAlquilerCreateView.as_view(), name="pagar_alquiler_crear"),
   # path('alquiler/<int:pk>',PagoAlquilerDetailView.as_view(), name="Pago_alquiler"),
  #  path('modificar/<int:pk>', PagoAlquilerUpdateView.as_view(), name="pago_alquiler_actualizar"),
  #  path('mostrar/',PagosAlquilieresListView.as_view(), name="pago_alquiler_listar"),
]