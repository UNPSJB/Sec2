# --------- CONSTANTES PARA LOS ROLES -----------
ROL_TIPO_AFILIADO = 1
ROL_TIPO_FAMILIAR = 2

# -------------- ICONOS ------------------------------------------
ICON_ERROR = '<i class="fa-solid fa-x fa-beat-fade"></i>'
ICON_CHECK = '<i class="fa-solid fa-square-check fa-beat-fade"></i>'
ICON_TRIANGLE = '<i class="fa-solid fa-triangle-exclamation fa-flip"></i>'

#---------------- MENSAJES DE DJANGO MESSAGE --------------------
# MENSAJES GENERICOS
MSJ_EXITO_MODIFICACION = 'Modificación exitosa!'
MSJ_CORRECTION = 'Por favor, corrija los errores a continuación.'
MSJ_ERROR_VALIDACION = 'Error en la validación de datos de la persona.'

# MENSAJE ESPECIFICO DE PERSONA
MSJ_PERSONA_NO_EXISTE = 'La persona no está registrada en el sistema.'
MSJ_PERSONA_EXISTE = 'Ya existe una persona registrada en el sistema con el mismo DNI.'

#MENSAJES ESPECIFICOS AFILIADO
MSJ_AFILIADO_DESAFILIADO = 'Se ha desafiliado.'
MSJ_CORRECTO_ALTA_AFILIADO = 'Alta de afiliado exitosa!'
MSJ_AFILIADO_AFILIADO = 'El afiliado ha sido aceptado.'
MSJ_AFILIADO_NO_FAMILIAR = 'El afiliado no tiene a este familiar.'

#MENSAJES ESPECIFICOS FAMILIAR
MSJ_FAMILIAR_CARGA_CORRECTA = 'Carga de familiar exitosa!'
MSJ_FAMILIAR_ELIMINADO = 'Familiar dado de baja.'
MSJ_FAMILIAR_ESPOSA_EXISTE = 'Ya existe un esposo/a para el afiliado asociado.'
MSJ_HIJO_MAYOR_EDAD = 'El Hijo/a debe ser menor de edad.'

#---------------- MENSAJES DE DJANGO MESSAGE --------------------
MAXIMO_PAGINATOR = 10


PERIODO_PAGO=(
        (1, 'mes'),
        (2, 'clase'),
    )

OPCIONES_CERTIFICADO = [
        (1, 'Sí'),
        (2, 'No'),
        (3, 'Opcional'),
]

