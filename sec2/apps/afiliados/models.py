from django.db import models
from apps.cursos.models import Dictado
from apps.personas.models import Rol
from utils.choices import AFILIADO_ESTADO, LOCALIDADES_CHUBUT, TIPOS_RELACION_FAMILIAR
from utils.constants import *
from utils.funciones import validate_no_mayor_actual
from utils.regularexpressions import *

# -------------------- FAMILIAR ------------------
class Familiar(Rol):
    TIPO = ROL_TIPO_FAMILIAR  # Define un valor único para el tipo de rol de Familiar
    activo = models.BooleanField(default=False)  # Agregamos el campo "activo" con valor predeterminado True
    dictados = models.ManyToManyField(Dictado, related_name="familiares", blank=True)
    lista_espera = models.ManyToManyField(Dictado, related_name='familiares_en_espera', blank=True)
    
    def __str__(self):
        return f"Activo: {self.activo}"

Rol.register(Familiar)

# -------------------- AFILIADO ------------------
class Afiliado(Rol):
    #Utilizado para Rol
    TIPO = ROL_TIPO_AFILIADO
    estado = models.PositiveSmallIntegerField(choices=AFILIADO_ESTADO, default=1)
    razon_social = models.CharField(max_length=30, validators=[text_and_numeric_validator])
    categoria_laboral = models.CharField(max_length=20, validators=[text_and_numeric_validator])
    rama = models.CharField(max_length=50, validators=[text_and_numeric_validator])
    sueldo = models.IntegerField(validators=[MinValueValidator(0, 'El sueldo debe ser un valor positivo.')])
    horaJornada = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cuit_empleador = models.CharField(max_length=11, validators=[numeric_validator], help_text='Cuit sin puntos y guiones. Ej: 01234567899')
    domicilio_empresa = models.CharField(max_length=50, validators=[text_and_numeric_validator], help_text='Calle y numero')

    fechaAfiliacion= models.DateField(
        null=True,
        blank=False,
        validators=[validate_no_mayor_actual]
    )
    fechaIngresoTrabajo = models.DateField(
        null=False,
        blank=False,
        validators=[validate_no_mayor_actual]
    )
    localidad_empresa = models.CharField(
        max_length=30,
        choices=LOCALIDADES_CHUBUT,
        default="TRELEW",
    )

    dictados = models.ManyToManyField(Dictado, related_name="afiliados", blank=True)
    lista_espera = models.ManyToManyField(Dictado, related_name='afiliados_en_espera', blank=True)
    familia = models.ManyToManyField(Familiar, through='RelacionFamiliar', blank=True)

    def __str__(self):
        return f" Tipo: {self.TIPO} Razon social: {self.razon_social} CUIT:{self.cuit_empleador}"
    
    def __strextra__(self):
        # Define your new string representation here
        return f"{self.persona.dni} | {self.persona}"
    
    def tiene_esposo(self):
        esposo_existente = self.familia.filter(tipo_relacion=1).exists()
        return esposo_existente
    
    """una vez activado al afiliado pondra a los familiares en estado de activo"""
    def activar_familiares(self):
        familiares = self.familia.all()
        for familiar in familiares:
            familiar.activo = True
            familiar.save()

Rol.register(Afiliado)

# -------------------- RELACION FAMILIAR-AFILIADO ------------------
class RelacionFamiliar(models.Model):
    afiliado = models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    familiar = models.ForeignKey(Familiar, on_delete=models.CASCADE)
    tipo_relacion = models.PositiveSmallIntegerField(choices=TIPOS_RELACION_FAMILIAR)

    def __str__(self):
        return f"Relación: {self.get_tipo_relacion_display()}"