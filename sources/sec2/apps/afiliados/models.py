from django.db import models
#from apps import personas
from apps.personas.models import Rol
from datetime import date

# Create your models here.
class Afiliado(Rol):
    TIPO = 1
    razon_social = models.CharField(max_length=50)
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


class MiModelo(models.Model):
    campo1 = models.CharField(max_length=100)
    # campo2 = models.IntegerField()
    # campo3 = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.campo1  # Esto define la representación en cadena del objeto

    # Puedes agregar métodos personalizados u otras configuraciones aquí
