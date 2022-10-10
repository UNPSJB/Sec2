
from django.db import models
#from apps import personas
from apps.personas.models import Rol

# Create your models here.
class Afiliado(Rol):
    TIPO = 1
    razon_social = models.CharField(max_length=50)
    cuit_empleador = models.CharField(max_length=8)
    categoria_laboral = models.CharField(max_length=20)
    domicilio_empresa = models.CharField(max_length=50)
    localidad_empresa = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)

    def __str__(self):
        return f"Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"
    

