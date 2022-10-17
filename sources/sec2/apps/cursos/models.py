from django.db import models

# Create your models here.
from apps.personas.models import Rol

class Alumno(Rol):
    legajo = models.CharField(max_length=10)

Rol.register(Alumno)

class Curso(models.Model):
    pass