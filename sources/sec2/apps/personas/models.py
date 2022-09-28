from django.db import models




class Persona(models.Model):
    ESTADO_CIVIL=(
        (1, 'soltero'),
        (2, 'casado'),
        (3, 'viudo'),
    )
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    dni=models.BigIntegerField(unique=True)
    direccion=models.CharField(max_length=50)
    mail=models.CharField(max_length=50)
    nacionalidad=models.CharField(max_length=50)
    estado_civil=models.PositiveSmallIntegerField(choices=ESTADO_CIVIL)
    cuil=models.BigIntegerField()
    celular=models.BigIntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"
