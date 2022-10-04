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
    celular=models.BigIntegerField(unique=True)
    encargado=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"

class Rol(models.Model):
    TIPO = 0
    TIPOS = [
        (1, "afiliado"),
        (2, "profesor"),
        (3, "alumno")
    ]
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateTimeField(auto_now_add=True)
    hasta = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.persona} es {self.get_tipo_display()}"

    def save(self, args, kwargs):
        if self.pk is None:
            self.tipo = Rol.TIPO
        super(Rol, self).save(args, kwargs)

    def related(self):
        return self.Rol != Rol and self or getattr(self, self.get_tipo_display())

    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.name.lower()))
    
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