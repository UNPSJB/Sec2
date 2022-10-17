from random import choices
from django.db import models
from apps import afiliados

class Persona(models.Model):
    ESTADO_CIVIL=(
        (1, 'soltero'),
        (2, 'casado'),
        (3, 'viudo'),
    )
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    dni=models.CharField(max_length=8)
    direccion=models.CharField(max_length=50)
    mail=models.CharField(max_length=50)
    nacionalidad=models.CharField(max_length=50)
    estado_civil=models.PositiveSmallIntegerField(choices=ESTADO_CIVIL)
    cuil=models.CharField(max_length=8)
    celular=models.CharField(max_length=30)
    encargado=models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"

    def afiliar(self, afiliado):
        afiliado.persona = self
        afiliado.save()

    def registrar_en_curso(self, alumno, curso):
        alumno.persona = self
        alumno.save()
        curso.alumnos.add(alumno)

class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateTimeField(auto_now_add=True)
    hasta = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.persona} es {self.get_tipo_display()}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = Rol.TIPO
        super(Rol, self).save(*args, **kwargs)

    def related(self):
        return self.Rol != Rol and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, Klass):
        cls.TIPOS.append((Klass.TIPO, Klass.__name__.lower()))
    
    def como(self, Klass):
        return self.roles.get(tipo=Klass.TIPO).related()

    def agregar_rol(self, rol):
        if not self.sos(rol.Rol):
            rol.persona = self
            rol.save()

    def roles_related(self):
        return [rol.related() for rol in self.roles.all()]

    def sos(self, Klass):
        return any([isinstance(rol, Klass) for rol in self.roles_related()])

class Familiar(models.Model):
    #se limita a familiares a los familiares hasta segunda linia 
    TIPOS=(
        (0,"hijo"),
        (1,"conyuge"),
        (2,"padre"),
        (3,"madre"),
        (4,"hermano"),
    )
    persona=models.ForeignKey(Persona, relate_name="familiar",on_delete=models.CASCADE)
    tipo=models.PositiveSmallIntegerField(choices=TIPOS)
