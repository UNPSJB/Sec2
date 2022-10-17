from email.policy import default
from msilib.schema import Class
from pickle import TRUE
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Actividades(models.Model):
    nombre=models.CharField(max_length=50)
    area=models.CharField(max_length=50)

    
