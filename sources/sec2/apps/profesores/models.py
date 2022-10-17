from email.policy import default
from pickle import TRUE
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Profesor(models.Model):
    capacitaciones = models.CharField(max_length=50)
   # ejerceDesde = models.DateField()
    #actividades = models.ArrayField(base_field=50)
    

