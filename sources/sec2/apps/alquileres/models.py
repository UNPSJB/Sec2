from unittest.util import _MAX_LENGTH
from django.db import models
from apps.personas.models import *
from apps.afiliados.models import *

# Create your models here.
class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    localidad=models.CharField(max_length=50)
    direccion=models.CharField(max_length=50)
    capacidad=models.PositiveIntegerField(help_text="capacidad maxima del salon")
    encargado=models.ForeignKey(Persona, related_name="salon", on_delete=models.CASCADE)
    precio=models.DecimalField(help_text="costo del alquiler", max_digits=10, decimal_places=2)
    fecha_baja=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #servicios [1..n]
    #tipo


class Alquiler(models.Model):
    afiliado=models.ForeignKey(Afiliado, related_name="alquileres", on_delete=models.CASCADE)
    salon=models.ForeignKey(Salon, related_name="alquileres", on_delete=models.CASCADE)
    fecha_solicitud=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_alquiler=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #servicios[1..n]

class Pago_alquiler(models.Model):
    alquiler=models.ForeignKey(Alquiler, related_name="pagos", on_delete=models.CASCADE)
    fecha_pago=models.DateTimeField(auto_now_add=True, null=True, blank=True)
