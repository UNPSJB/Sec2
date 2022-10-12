from django.db import models

from apps.personas.models import Rol

class Alumno(Rol):
    legajo = models.CharField(max_length=10)

Rol.register(Alumno)

class Curso(models.Model):
    pass