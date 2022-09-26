from django.db import models


# Create your models here.
class Persona(models.Model):

    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    dni=models.BigIntegerField(primary_key=True)
    direccion=models.CharField(max_length=50)
    mail=models.CharField(max_length=50)
    nacionalidad=models.CharField(max_length=50)
    estado_civil=models.BooleanField()
    cuil=models.BigIntegerField()
    celular=models.BigIntegerField()

def __str__(self):
    return self.nombre + ' ' + self.apellido + ' ' + self.dni
