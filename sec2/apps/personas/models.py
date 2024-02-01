from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from utils.constants import *
from utils.regularexpressions import *


class Persona(models.Model):
    dni = models.CharField(
        max_length=8,
        help_text='DNI sin puntos. Ej: 12345678',
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',  # Expresión regular para 8 dígitos
                message=f'{XMARK_ICON} El DNI debe tener exactamente 8 dígitos.',
                code='invalid_dni_format',
            ),
            is_numeric,  # Validador personalizado para verificar si es un número
        ],
    )
    cuil = models.CharField(
        max_length=11,
        help_text='Sin puntos y guiones. Ej: 01234567890',
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',  # Expresión regular para 11 dígitos
                message=f'{XMARK_ICON} El CUIL debe tener exactamente 11 dígitos.',
                code='invalid_cuil_format',
            ),
            is_numeric,  # Validador personalizado para verificar si es un número
        ],
    )
    nombre = models.CharField(max_length=30, validators=[text_validator])
    apellido = models.CharField(max_length=30, validators=[text_validator])

    def validate_fecha_nacimiento(value):
        if value > timezone.now().date():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')

    fecha_nacimiento = models.DateField(
        null=False,
        blank=False,
        validators=[validate_fecha_nacimiento]
    )

    celular = models.CharField(
        max_length=13,  # Máximo 12 caracteres para ###-########
        validators=[numeric_validator],
        help_text='549XXXXXXXXX, 0XX-XXXXXXXX o 15XXXXXXXXX.'
    )
    
    direccion = models.CharField(max_length=50, validators=[text_and_numeric_validator], help_text='Calle y numero')
    nacionalidad = models.CharField(
        max_length=2,
        choices=NACIONALIDADES,
        default="AR",
    )
    
    mail = models.EmailField(
        max_length=50,
        validators=[EmailValidator(message='Debe ser un correo válido.')],
        help_text='Debe ser un correo válido.'
    )
    estado_civil = models.PositiveSmallIntegerField(choices=ESTADO_CIVIL)
    es_afiliado = models.BooleanField(default=False)
    es_alumno = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)
    es_encargado = models.BooleanField(default=False)
    familia = models.ManyToManyField('self', through='Vinculo', blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.dni} {self.nombre} {self.apellido}"

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

# class Familiar(models.Model):
#     #se limita a familiares a los familiares hasta segunda linia 
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
    
class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateTimeField(auto_now_add=True)
    hasta = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.persona} es {self.get_tipo_display()}"

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