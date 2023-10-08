from random import choices
from tokenize import blank_re
from django.db import models
from apps import afiliados, cursos
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

XMARK_ICON = '<i class="fa-solid fa-xmark"></i>'

class Persona(models.Model):
    ESTADO_CIVIL = (
        (1, 'soltero'),
        (2, 'casado'),
        (3, 'viudo'),
    )

    # Arreglo amplio de nacionalidades
    NACIONALIDADES = [
    ("AF", "Afganistán"),
    ("AL", "Albania"),
    ("DE", "Alemania"),
    ("AD", "Andorra"),
    ("AO", "Angola"),
    ("AI", "Anguila"),
    ("AQ", "Antártida"),
    # ("AG", "Antigua y Barbuda"),
    # ("AN", "Antillas Neerlandesas"),
    ("SA", "Arabia Saudita"),
    ("DZ", "Argelia"),
    ("AR", "Argentina"),
    ("AM", "Armenia"),
    ("AW", "Aruba"),
    ("AU", "Australia"),
    ("AT", "Austria"),
    ("AZ", "Azerbaiyán"),
    ("BS", "Bahamas"),
    ("BH", "Bahréin"),
    ("BD", "Bangladesh"),
    ("BB", "Barbados"),
    ("BE", "Bélgica"),
    ("BZ", "Belice"),
    ("BJ", "Benín"),
    ("BM", "Bermudas"),
    ("BY", "Bielorrusia"),
    ("MM", "Birmania"),
    ("BO", "Bolivia"),
    # ("BA", "Bosnia y Herzegovina"),
    ("BW", "Botsuana"),
    ("BR", "Brasil"),
    ("BN", "Brunéi"),
    ("BG", "Bulgaria"),
    ("BF", "Burkina Faso"),
    ("BI", "Burundi"),
    ("BT", "Bután"),
    ("CV", "Cabo Verde"),
    ("KH", "Camboya"),
    ("CM", "Camerún"),
    ("CA", "Canadá"),
    ("TD", "Chad"),
    ("CL", "Chile"),
    ("CN", "China"),
    ("CY", "Chipre"),
    # ("VA", "Ciudad del Vaticano"),
    ("CO", "Colombia"),
    ("KM", "Comoras"),
    ("CG", "Congo"),
    # ("CD", "Congo, República Democrática del"),
    ("KP", "Corea del Norte"),
    ("KR", "Corea del Sur"),
    ("CI", "Costa de Marfil"),
    ("CR", "Costa Rica"),
    ("HR", "Croacia"),
    ("CU", "Cuba"),
    ("DK", "Dinamarca"),
    ("DM", "Dominica"),
    ("EC", "Ecuador"),
    ("EG", "Egipto"),
    ("SV", "El Salvador"),
    ("AE", "Emiratos Árabes"),
    ("ER", "Eritrea"),
    ("SK", "Eslovaquia"),
    ("SI", "Eslovenia"),
    ("ES", "España"),
    ("US", "Estados Unidos"),
    ("EE", "Estonia"),
    ("ET", "Etiopía"),
    ("PH", "Filipinas"),
    ("FI", "Finlandia"),
    ("FJ", "Fiyi"),
    ("FR", "Francia"),
    ("GA", "Gabón"),
    ("GM", "Gambia"),
    ("GE", "Georgia"),
    ("GH", "Ghana"),
    ("GI", "Gibraltar"),
    ("GD", "Granada"),
    ("GR", "Grecia"),
    ("GL", "Groenlandia"),
    ("GP", "Guadalupe"),
    ("GU", "Guam"),
    ("GT", "Guatemala"),
    ("GY", "Guayana"),
    ("GF", "Guayana Francesa"),
    ("GN", "Guinea"),
    ("GQ", "Guinea Ecuatorial"),
    ("GW", "Guinea-Bisáu"),
    ("HT", "Haití"),
    ("HN", "Honduras"),
    ("HU", "Hungría"),
    ("IN", "India"),
    ("ID", "Indonesia"),
    ("IR", "Irán"),
    ("IQ", "Iraq"),
    ("IE", "Irlanda"),
    ("IS", "Islandia"),
    ("IL", "Israel"),
    ("IT", "Italia"),
    ("JM", "Jamaica"),
    ("JP", "Japón"),
    ("JO", "Jordania"),
    ("KZ", "Kazajistán"),
    ("KE", "Kenia"),
    ("KG", "Kirguistán"),
    ("KW", "Kuwait"),
    ("LA", "Laos"),
    ("LS", "Lesoto"),
    ("LV", "Letonia"),
    ("LB", "Líbano"),
    ("LR", "Liberia"),
    ("LY", "Libia"),
    ("LI", "Liechtenstein"),
    ("LT", "Lituania"),
    ("LU", "Luxemburgo"),
    ("MK", "Macedonia"),
    ("MG", "Madagascar"),
    ("MY", "Malasia"),
    ("MW", "Malaui"),
    ("MV", "Maldivas"),
    ("ML", "Malí"),
    ("MT", "Malta"),
    ("MA", "Marruecos"),
    ("MQ", "Martinica"),
    ("MU", "Mauricio"),
    ("MR", "Mauritania"),
    ("YT", "Mayotte"),
    ("MX", "México"),
    ("FM", "Micronesia"),
    ("MD", "Moldavia"),
    ("MC", "Mónaco"),
    ("MN", "Mongolia"),
    ("MS", "Montserrat"),
    ("MZ", "Mozambique"),
    ("NA", "Namibia"),
    ("NR", "Nauru"),
    ("NP", "Nepal"),
    ("NI", "Nicaragua"),
    ("NE", "Níger"),
    ("NG", "Nigeria"),
    ("NU", "Niue"),
    ("NF", "Norfolk"),
    ("NO", "Noruega"),
    ("NC", "Nueva Caledonia"),
    ("NZ", "Nueva Zelanda"),
    ("OM", "Omán"),
    ("NL", "Países Bajos"),
    ("PA", "Panamá"),
    ("PG", "Papúa Nueva Guinea"),
    ("PK", "Pakistán"),
    ("PY", "Paraguay"),
    ("PE", "Perú"),
    ("PN", "Pitcairn"),
    ("PF", "Polinesia Francesa"),
    ("PL", "Polonia"),
    ("PT", "Portugal"),
    ("PR", "Puerto Rico"),
    ("QA", "Qatar"),
    ("UK", "Reino Unido"),
    # ("CF", "República Centroafricana"),
    ("CZ", "República Checa"),
    ("DO", "República Dominicana"),
    ("RE", "Reunión"),
    ("RW", "Ruanda"),
    ("RO", "Rumania"),
    ("RU", "Rusia"),
    ("EH", "Sahara Occidental"),
    ("WS", "Samoa"),
    ("AS", "Samoa Americana"),
    # ("KN", "San Cristóbal y Nieves"),
    ("SM", "San Marino"),
    ("PM", "San Pedro y Miquelón"),
    # ("VC", "San Vicente y las Granadinas"),
    ("SH", "Santa Elena"),
    ("LC", "Santa Lucía"),
    ("ST", "Santo Tomé y Príncipe"),
    ("SN", "Senegal"),
    ("CS", "Serbia y Montenegro"),
    ("SC", "Seychelles"),
    ("SL", "Sierra Leona"),
    ("SG", "Singapur"),
    ("SY", "Siria"),
    ("SO", "Somalia"),
    ("LK", "Sri Lanka"),
    ("SZ", "Suazilandia"),
    ("ZA", "Sudáfrica"),
    ("SD", "Sudán"),
    ("SE", "Suecia"),
    ("CH", "Suiza"),
    ("SR", "Surinam"),
    # ("SJ", "Svalbard y Jan Mayen"),
    ("TH", "Tailandia"),
    ("TW", "Taiwán"),
    ("TZ", "Tanzania"),
    ("TJ", "Tayikistán"),
    # ("IO", "Territorio Británico del Océano Índico"),
    # ("TF", "Territorios Australes Franceses"),
    ("TL", "Timor Oriental"),
    ("TG", "Togo"),
    ("TK", "Tokelau"),
    ("TO", "Tonga"),
    ("TT", "Trinidad y Tobago"),
    ("TN", "Túnez"),
    ("TM", "Turkmenistán"),
    ("TR", "Turquía"),
    ("TV", "Tuvalu"),
    ("UA", "Ucrania"),
    ("UG", "Uganda"),
    ("UY", "Uruguay"),
    ("UZ", "Uzbekistán"),
    ("VU", "Vanuatu"),
    ("VE", "Venezuela"),
    ("VN", "Vietnam"),
    ("WF", "Wallis y Futuna"),
    ("YE", "Yemen"),
    ("DJ", "Yibuti"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabue"),
    ]

    numeric_validator = RegexValidator(
        regex=r'^\d+$',
        message=f'{XMARK_ICON} Debe contener solo dígitos numéricos.',
        # message='<i class="fa-solid fa-xmark"></i> Debe contener solo dígitos numéricos.',
        code='invalid_numeric'
    )

    text_validator = RegexValidator(
        regex=r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
        message=f'{XMARK_ICON} Debe contener letras y espacios.',
        code='invalid_text'
    )

    text_and_numeric_validator = RegexValidator(
    regex=r'^[A-Za-z0-9\s]+$',
    message=f'{XMARK_ICON} Sin caracteres especiales.',
    code='invalid_text'
)

    celular_validator = RegexValidator(
        regex=r'^\d{3}-\d{8}$',
        message=f'{XMARK_ICON} Número no válido',
        code='invalid_celular_argentino'
    )

    dni = models.CharField(max_length=8, validators=[numeric_validator], help_text='Dni sin puntos. Ej: 12345678')
    cuil = models.CharField(max_length=11, validators=[numeric_validator], help_text='Cuil sin puntos y sin guiones. Ej: 01234567890')
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
        max_length=12,  # Máximo 12 caracteres para ###-########
        validators=[celular_validator],
        help_text='Formato ###-########.'
    )
    
    direccion = models.CharField(max_length=50, validators=[text_and_numeric_validator])
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
        return f"{self.nombre} {self.apellido} DNI:{self.dni}"

    #convierte una persona en profesor
    def convertir_en_profesor(self, profesor):
        assert not self.es_profesor, "ya soy Profesor" 
        profesor.persona = self
        profesor.save()
        self.es_profesor=True
        self.save()

    def afiliar(self, afiliado, fecha):
        print("ESTOY EN AFILIAR DE Persona")
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

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
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