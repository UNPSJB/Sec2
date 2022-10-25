from random import choices
from tokenize import blank_re
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
    es_afiliado=models.BooleanField(default=False)
    es_alumno=models.BooleanField(default=False)
    es_profesor=models.BooleanField(default=False)
    es_encargado=models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=False ,blank=False)
    
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"

    def afiliar(self, afiliado):
        assert not self.es_afiliado, "ya soy afiliado" 
        afiliado.persona = self
        afiliado.save()
        self.es_afiliado=True
        self.save()
        
    def desafiliar(self, afiliado, fecha):
        assert afiliado.persona == self, "Afiliado incorrecto"
        afiliado.hasta = fecha
        afiliado.save()
        self.es_afiliado = False
        self.save()
        
    def inscribir(self, alumno, curso):
        assert alumno.curso == curso, "Alumno ya inscripto"
        alumno.persona = self
        alumno.save()
        curso.alumnos.add(alumno)
        self.es_alumno=True
        self.save()

    def desinscribir(self, alumno, fecha):
        assert alumno.persona == self, "alumno equivocado"
        alumno.hasta = fecha
        alumno.save()
        
        self.es_alumno = False
        self.save()
        
    
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
        (1,"hijo"),
        (2,"conyuge"),
        (3,"padre"),
        (4,"madre"),
        (5,"hermano"),
        (6,"tutor"),
    )
    AFILIADO = [1, 2, 3, 4, 5]
    ALUMNO = [3, 4, 6]
    persona=models.ForeignKey(Persona, related_name="familiar",on_delete=models.CASCADE)
    tipo=models.PositiveSmallIntegerField(choices=TIPOS)


    
