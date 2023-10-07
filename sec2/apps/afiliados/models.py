from django.db import models
from apps.personas.models import Rol
from datetime import date
from django import forms
from django.core.validators import RegexValidator

# Create your models here.
class Afiliado(Rol):
    TIPO = 1
    razon_social = models.CharField(max_length=50)
   #  cuit_empleador = models.CharField(
   #     max_length=10,
   #     validators=[
   #        RegexValidator(
   #           regex=r'^\d{11}$',  # Expresión regular para validar un CUIT
   #           message='El CUIT debe contener exactamente 11 dígitos numéricos.',
   #           code='invalid_cuit'
   #           )
   #           ]
   #  )
    cuit_empleador = models.CharField(max_length=10)
    categoria_laboral = models.CharField(max_length=20)
    domicilio_empresa = models.CharField(max_length=50)
    localidad_empresa = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    fechaIngresoTrabajo = models.DateField()
    sueldo= models.DecimalField(max_digits=9, decimal_places=2)
    horaJornada = models.PositiveIntegerField()
    fechaAfiliacion= models.DateField()
    
    ESTADO = (
        (1, "pendiente de aceptación"), 
        (2, "activo"),
        (3, "inactivo"),
        )
    estado = models.PositiveSmallIntegerField(choices=ESTADO)
    
    def __str__(self):
        return f"Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"

Rol.register(Afiliado)
