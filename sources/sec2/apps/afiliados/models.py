from email.policy import default
from pickle import TRUE
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Afiliado(models.Model):
    razon_social = models.CharField(max_length=50)
    cuit_empleador = models.CharField(max_length=8)
    categoria_laboral = models.CharField(max_length=20)
    domicilio_empresa = models.CharField(max_length=50)
    localidad_empresa = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()
    fechaIngresoTrabajo = models.DateField()
    sueldo= models.DecimalField(max_digits=9, decimal_places=2)
    horaJornada = models.PositiveIntegerField()
    fechaAfiliacion= models.DateField()
    estado = models.BooleanField(default=False)
