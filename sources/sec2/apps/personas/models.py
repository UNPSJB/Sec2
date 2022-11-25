from random import choices
from tokenize import blank_re
from django.db import models
from apps import afiliados, cursos

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
    cuil=models.CharField(max_length=11)
    celular=models.CharField(max_length=30)
    es_afiliado=models.BooleanField(default=False)
    es_alumno=models.BooleanField(default=False)
    es_profesor=models.BooleanField(default=False)
    es_encargado=models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=False ,blank=False)
    familia = models.ManyToManyField('self', through='Vinculo', null=True, blank=True)
    #familia = models.ManyToManyField('self', through='Familiar')

    
    def __str__(self):
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"

    
    #convierte una persona en profesor
    def convertir_en_profesor(self, profesor):
        assert not self.es_profesor, "ya soy Profesor" 
        profesor.persona = self
        profesor.save()
        self.es_profesor=True
        self.save()

    def afiliar(self, afiliado, fecha):
        assert not self.es_afiliado, "ya soy afiliado" 
        afiliado.desde = fecha
        afiliado.persona = self
        afiliado.estado = 1
        afiliado.save()
        self.es_afiliado=True
        self.save()
        
    def desafiliar(self, afiliado, fecha):
        assert afiliado.persona == self, "Afiliado incorrecto"
        afiliado.hasta = fecha
        afiliado.save()
        afiliado.estado = 3
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



class Vinculo (models.Model): 
    CONYUGE=0
    HIJO=1
    TUTOR=2
    TIPO = [(0, "Conyuge"), (1,"Hijo"), (2,"Tutor")] 
    tipoVinculo = models.PositiveSmallIntegerField(choices = TIPO)
    vinculante = models.ForeignKey(Persona, related_name = "vinculados", on_delete = models.CASCADE) 
    vinculado = models.ForeignKey(Persona, related_name = "vinculantes",  on_delete = models.CASCADE) 

    def __str__(self):
        return f"{self.vinculado} es {self.get_tipoVinculo_display()}"


    
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

#class Familiar(models.Model):
    #se limita a familiares a los familiares hasta segunda linia 
#    TIPOS=(
#        (1,"hijo"),
#        (2,"conyuge"),
#        (3,"padre"),
#        (4,"madre"),
#        (5,"hermano"),
#        (6,"tutor"),
#    )
#    AFILIADO = [1, 2, 3, 4, 5]
#    ALUMNO = [3, 4, 6]
#    persona=models.ForeignKey(Persona, related_name = "familiares", on_delete = models.CASCADE) 
#    familiar_de=models.ForeignKey(Persona, related_name = "personas", on_delete = models.CASCADE) 
#    tipo=models.PositiveSmallIntegerField(choices=TIPOS)



    
