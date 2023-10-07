from django.db import models
from apps.cursos.models import Alumno

# Create your models here.

class Pago_alumno(models.Model):
    alumno= models.ForeignKey(Alumno, related_name="pagos", on_delete=models.CASCADE)
    #to do: fecha, importe 