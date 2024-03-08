# --------- CONSTANTES PARA LOS ROLES -----------
ROL_TIPO_AFILIADO = 1
ROL_TIPO_FAMILIAR = 2
ROL_TIPO_ALUMNO = 3
ROL_TIPO_PROFESOR = 4
ROL_TIPO_ENCARGADO = 5

# -------------- ICONOS ------------------------------------------
ICON_ERROR = '<i class="fa-solid fa-x fa-beat-fade"></i>'
ICON_CHECK = '<i class="fa-solid fa-square-check fa-beat-fade"></i>'
ICON_TRIANGLE = '<i class="fa-solid fa-triangle-exclamation fa-flip"></i>'

#---------------- MENSAJES DE DJANGO MESSAGE --------------------
# MENSAJES GENERICOS
MSJ_EXITO_MODIFICACION = 'Modificación exitosa!'
MSJ_CORRECTION = 'Por favor, corrija los errores a continuación.'
MSJ_ERROR_VALIDACION = 'Error en la validación de datos de la persona.'

MSJ_NOMBRE_EXISTE = 'El nombre ya existe o posee caracteres no deseados.'
MSJ_TIPO_NUMERO_EXISTE = 'El tipo y numero de aula ya existe.'
MSJ_ERROR_ELIMINAR = 'Ocurrió un error al intentar eliminar la actividad.'

# MENSAJE ESPECIFICO DE PERSONA
MSJ_PERSONA_NO_EXISTE = 'La persona no está registrada en el sistema.'
MSJ_PERSONA_EXISTE = 'Ya existe una persona activa registrada en el sistema con el mismo DNI.'

#MENSAJES ESPECIFICOS AFILIADO
MSJ_AFILIADO_DESAFILIADO = 'Se ha desafiliado al afiliado y a los familiares del mismo.'
MSJ_CORRECTO_ALTA_AFILIADO = 'Alta de afiliado exitosa!'
MSJ_AFILIADO_AFILIADO = 'El afiliado ha sido aceptado.'
MSJ_AFILIADO_NO_FAMILIAR = 'El afiliado no tiene a este familiar.'

#MENSAJES ESPECIFICOS FAMILIAR
MSJ_FAMILIAR_CARGA_CORRECTA = 'Carga de familiar exitosa!'
MSJ_FAMILIAR_ELIMINADO = 'Familiar dado de baja.'
MSJ_FAMILIAR_ESPOSA_EXISTE = 'Ya existe un esposo/a para el afiliado asociado.'
MSJ_HIJO_MAYOR_EDAD = 'El Hijo/a debe ser menor de edad.'

#MENSAJE ESPECIFICO PARA AULAS
MSJ_ACTIVIDAD_ALTA_EXITOSA = 'Alta de actividad exitosa!.'
MSJ_ACTIVIDAD_EXITO_BAJA = ' La actividad se se eliminó correctamente!.'

#MENSAJE ESPECIFICO PARA AULAS
MSJ_AULA_ALTA_EXITOSA = 'Alta de Actividad exitosa!.'
MSJ_AULA_EXITO_BAJA = ' La Actividad se se eliminó correctamente!.'


#MENSAJE ESPECIFIOC PARA PROFESOR
MSJ_CORRECTO_ALTA_PROFESOR = 'Profesor dado de alta con éxito!'


# MENSAJE ESPECIFICO PARA ENCARGADO
MSJ_CORRECTO_ALTA_ENCARGADO = 'Alta de encargado exitoso!'


# MENSAJE ESPECIFICO PARA SERVICIO
MSJ_SERVICIO_ALTA_EXITOSA = 'Servicio creado con exito!.'


# MENSAJE ESPECIFICO PARA AFILIADO
MSJ_CORRECTO_ALTA_SALON = 'Salon dado de alta con exito!'
#---------------- MENSAJES DE DJANGO MESSAGE --------------------
MAXIMO_PAGINATOR = 10




OPCIONES_CERTIFICADO = [
        (1, 'Sí'),
        (2, 'No'),
        (3, 'Opcional'),
]

