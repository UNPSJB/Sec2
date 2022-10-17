from email.policy import default
from pickle import TRUE
from unittest.util import _MAX_LENGTH
from django.db import models
from apps.personas.models import Rol
from apps.actividades import models

# Create your models here.
class Profesor(Rol):
    TIPO = 2
    capacitaciones = models.CharField(max_length=50)
    ejerceDesde = models.DateField()
    actividades = models.models.ManyToManyField(Actividades)
    

