document.addEventListener("DOMContentLoaded", function () {
    const errorIcon = '<i class="fa-solid fa-xmark"></i>';

    const btnSiguiente = document.getElementById("btn-siguiente");
    const btnAnterior = document.getElementById("btn-anterior");
    const datosPersonales = document.getElementById("datos-personales");
    const datosLaborales = document.getElementById("datos-laborales");
    const btnGuardar = document.getElementById("btn-guardar");

    // ------------------PRIMERA PARTE DEL FORMULARIO
    // Función para validar la fecha de nacimiento en tiempo real
    $(document).ready(function () {
        $('#fecha_nacimiento').on('change', function () {
            const fechaNacimiento = new Date($(this).val());
            const edad = new Date().getFullYear() - fechaNacimiento.getFullYear();

            if (edad < 18 || edad >= 100) {
                $('#fecha-nacimiento-error').html(errorIcon + ' Debes ser mayor de 18 años y menor de 100 años.');
            } else {
                $('#fecha-nacimiento-error').text('');
            }
        });
    });

    // Función para validar el correo electrónico en tiempo real
    function validarCorreoElectronico() {
        const emailInput = document.querySelector("#datos-personales input[name='mail']");
        const emailError = document.getElementById("email-error");
        const emailValue = emailInput.value.trim();

        // Expresión regular para validar un correo electrónico
        const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

        // Comprobar si el correo electrónico es válido
        if (emailRegex.test(emailValue)) {
            emailError.textContent = ""; // Correo electrónico válido, elimina el mensaje de error
        } else {
            emailError.innerHTML = errorIcon + ' Correo electrónico no válido.';
        }
    }
    const emailInput = document.querySelector("#datos-personales input[name='mail']");
    emailInput.addEventListener("input", validarCorreoElectronico);

    //Para poder pasar a mi siguiente formulario
    btnSiguiente.addEventListener("click", function () {
        // Comprobar si todos los campos requeridos en la sección actual están llenos
        const camposSeccionActual = document.querySelectorAll("#datos-personales input:required");
        const camposCompletos = Array.from(camposSeccionActual).every(function (campo) {
            return campo.value.trim() !== ""; // Verificar si el campo no está vacío
        });

        // Comprobar si la fecha de nacimiento y el correo electrónico son válidos
        const fechaNacimientoError = document.getElementById("fecha-nacimiento-error").textContent;
        const emailError = document.getElementById("email-error").textContent;
        const fechaValida = fechaNacimientoError === "";
        const emailValido = emailError === "";

        if (camposCompletos && fechaValida && emailValido) {
            // Ocultar Datos Personales y mostrar Datos Laborales
            datosPersonales.style.display = "none";
            btnSiguiente.style.display = "none";
            datosLaborales.style.display = "block";
            btnAnterior.style.display = "block";
            btnGuardar.style.display = "block";
        } else {
            if (!fechaValida) {
                alert("Por favor, corrija la fecha de nacimiento antes de continuar.");
            } else if (!emailValido) {
                alert("Por favor, corrija el correo electrónico antes de continuar.");
            } else {
                alert("Por favor, complete todos los campos requeridos antes de continuar.");
            }
        }
    });

    //SEGUNDO FORMULARIO DE DATOS DE AFILIACION

    // Función para validar la razon_social en tiempo real
    function validarRazonSocial() {
        const razonSocialInput = document.querySelector("#datos-laborales input[name='razon_social']");
        const razonSocialError = document.getElementById("razon-social-error");
        const razonSocialValue = razonSocialInput.value.trim();

        // Expresión regular para permitir letras, números y espacios
        const razonSocialRegex = /^[A-Za-z0-9\s]+$/;

        // Comprobar si la razon_social es válida
        if (razonSocialRegex.test(razonSocialValue)) {
            razonSocialError.textContent = ""; // razon_social válida, elimina el mensaje de error
        } else {
            razonSocialError.innerHTML = errorIcon + ' No debe contener caracteres especiales.';
        }
    }
    // Agregar event listener al campo de razon_social para validación en tiempo real
    const razonSocialInput = document.querySelector("#datos-laborales input[name='razon_social']");
    razonSocialInput.addEventListener("input", validarRazonSocial);

    // Función para validar la categoria_laboral en tiempo real
    function validarCategoriaLaboral() {
        const categoriaLaboralInput = document.querySelector("#datos-laborales input[name='categoria_laboral']");
        const categoriaLaboralError = document.getElementById("categoria-laboral-error");
        const categoriaLaboralErrorIcon = document.getElementById("categoria-laboral-error-icon"); // Icono de error
        const categoriaLaboralValue = categoriaLaboralInput.value.trim();

        // Expresión regular para permitir letras y espacios
        const categoriaLaboralRegex = /^[A-Za-z\s]+$/;

        // Comprobar si la categoria_laboral es válida
        if (categoriaLaboralRegex.test(categoriaLaboralValue)) {
            categoriaLaboralError.textContent = ""; // categoria_laboral válida, elimina el mensaje de error
            categoriaLaboralErrorIcon.style.display = "none"; // Oculta el icono de error
        } else {
            categoriaLaboralError.innerHTML = errorIcon + ' Solo debe contener letras y/o espacios.';
        }
    }
    // Agregar event listener al campo de categoria_laboral para validación en tiempo real
    const categoriaLaboralInput = document.querySelector("#datos-laborales input[name='categoria_laboral']");
    categoriaLaboralInput.addEventListener("input", validarCategoriaLaboral);

    // Función para validar la rama en tiempo real
    function validarRama() {
        const ramaInput = document.querySelector("#datos-laborales input[name='rama']");
        const ramaError = document.getElementById("rama-error");
        const ramaValue = ramaInput.value.trim();

        // Expresión regular para permitir letras y espacios
        const ramaRegex = /^[A-Za-z\s]+$/;

        // Comprobar si la rama es válida
        if (ramaRegex.test(ramaValue)) {
            ramaError.textContent = ""; // rama válida, elimina el mensaje de error
        } else {
            ramaError.innerHTML = errorIcon + ' Solo debe contener letras y/o espacios.';
        }
    }
    // Agregar event listener al campo de rama para validación en tiempo real
    const ramaInput = document.querySelector("#datos-laborales input[name='rama']");
    ramaInput.addEventListener("input", validarRama);

    // Función para validar el sueldo en tiempo real
    function validarSueldo() {
        const sueldoInput = document.querySelector("#datos-laborales input[name='sueldo']");
        const sueldoError = document.getElementById("sueldo-error");
        const sueldoValue = sueldoInput.value.trim();

        // Expresión regular para permitir números positivos con hasta dos decimales
        const sueldoRegex = /^\d+(\.\d{1,2})?$/;

        // Comprobar si el sueldo es válido
        if (sueldoRegex.test(sueldoValue) && parseFloat(sueldoValue) >= 0) {
            sueldoError.textContent = ""; // Sueldo válido, elimina el mensaje de error
        } else {
            sueldoError.innerHTML = errorIcon + ' Solo numeros positivos con hasta dos decimales.';
        }
    }
    const sueldoInput = document.querySelector("#datos-laborales input[name='sueldo']");
    sueldoInput.addEventListener("input", validarSueldo);

    // Función para validar la fecha de afiliación en tiempo real
    function validarFechaAfiliacion() {
        const fechaAfiliacionInput = document.querySelector("#datos-laborales input[name='fechaAfiliacion']");
        const fechaAfiliacionError = document.getElementById("fecha-fechaAfiliacion-error");
        const fechaAfiliacionValue = fechaAfiliacionInput.value.trim();

        // Obtener la fecha actual
        const fechaActual = new Date();
        fechaActual.setHours(0, 0, 0, 0); // Establecer hora a 00:00:00:000 para comparación

        // Convertir la fecha de afiliación en un objeto Date
        const fechaAfiliacion = new Date(fechaAfiliacionValue);

        // Comprobar si la fecha de afiliación es válida y no es mayor que la fecha actual
        if (!isNaN(fechaAfiliacion.getTime()) && fechaAfiliacion <= fechaActual) {
            fechaAfiliacionError.textContent = ""; // Fecha de afiliación válida, elimina el mensaje de error
        } else {
            fechaAfiliacionError.innerHTML = errorIcon + ' La fecha no puede ser mayor que la fecha actual.';
        }
    }
    // Agregar event listener al campo de fecha de afiliación para validación en tiempo real
    const fechaAfiliacionInput = document.querySelector("#datos-laborales input[name='fechaAfiliacion']");
    fechaAfiliacionInput.addEventListener("input", validarFechaAfiliacion);

    //------------------- DATOS EMPRESARIALES
    // Función para validar la hora de la jornada en tiempo real
    function validarHoraJornada() {
        const horaJornadaInput = document.querySelector("#datos-laborales input[name='horaJornada']");
        const horaJornadaError = document.getElementById("hora-jornada-error");
        const horaJornadaValue = parseFloat(horaJornadaInput.value);

        // Comprobar si la hora de la jornada es mayor que 0
        if (horaJornadaValue > 0) {
            horaJornadaError.textContent = ""; // Hora de la jornada válida, elimina el mensaje de error
        } else {
            horaJornadaError.innerHTML = errorIcon + ' La hora de la jornada debe ser mayor que 0.';
        }
    }
    // Agregar event listener al campo de hora de la jornada para validación en tiempo real
    const horaJornadaInput = document.querySelector("#datos-laborales input[name='horaJornada']");
    horaJornadaInput.addEventListener("input", validarHoraJornada);

    // Función para validar la fecha de ingreso en tiempo real
    function validarFechaIngreso() {
        const fechaIngresoInput = document.querySelector("#datos-laborales input[name='fechaIngresoTrabajo']");
        const fechaIngresoError = document.getElementById("fecha-fechaIngresoTrabajo-error");
        const fechaIngresoValue = fechaIngresoInput.value.trim();

        // Obtener la fecha actual
        const fechaActual = new Date();
        fechaActual.setHours(0, 0, 0, 0); // Establecer hora a 00:00:00:000 para comparación

        // Convertir la fecha de ingreso en un objeto Date
        const fechaIngreso = new Date(fechaIngresoValue);

        // Comprobar si la fecha de ingreso es válida y no es mayor que la fecha actual
        if (!isNaN(fechaIngreso.getTime()) && fechaIngreso <= fechaActual) {
            fechaIngresoError.textContent = ""; // Fecha de ingreso válida, elimina el mensaje de error
        } else {

            fechaIngresoError.innerHTML = errorIcon + ' La fecha no puede ser mayor que la fecha actual.';
        }
    }
    // Agregar event listener al campo de fecha de ingreso para validación en tiempo real
    const fechaIngresoInput = document.querySelector("#datos-laborales input[name='fechaIngresoTrabajo']");
    fechaIngresoInput.addEventListener("input", validarFechaIngreso);

    // Función para validar el Cuit empleador en tiempo real
    function validarCuitEmpleador() {
        const cuitEmpleadorInput = document.querySelector("#datos-laborales input[name='cuit_empleador']");
        const cuitEmpleadorError = document.getElementById("cuit-empleador-error");
        const cuitEmpleadorValue = cuitEmpleadorInput.value.trim();

        // Expresión regular para permitir solo números
        const numerosRegex = /^[0-9]+$/;

        // Comprobar si el Cuit empleador es válido
        if (numerosRegex.test(cuitEmpleadorValue)) {
            cuitEmpleadorError.textContent = ""; // Cuit empleador válido, elimina el mensaje de error
        } else {
            cuitEmpleadorError.innerHTML = errorIcon + ' Solo se permiten números en el Cuit del empleador.';
        }
    }
    // Agregar event listener al campo de Cuit empleador para validación en tiempo real
    const cuitEmpleadorInput = document.querySelector("#datos-laborales input[name='cuit_empleador']");
    cuitEmpleadorInput.addEventListener("input", validarCuitEmpleador);

    // Función para validar la dirección de la empresa en tiempo real
    function validarDireccionEmpresa() {
        const direccionEmpresaInput = document.querySelector("#datos-laborales input[name='domicilio_empresa']");
        const direccionEmpresaError = document.getElementById("direccion-empresa-error");
        const direccionEmpresaValue = direccionEmpresaInput.value.trim();

        // Expresión regular para permitir letras, espacios y números
        const direccionEmpresaRegex = /^[A-Za-z0-9\s]+$/;

        // Comprobar si la dirección de la empresa es válida
        if (direccionEmpresaRegex.test(direccionEmpresaValue)) {
            direccionEmpresaError.textContent = ""; // Dirección de la empresa válida, elimina el mensaje de error
        } else {
            direccionEmpresaError.textContent = "No se aceptan caracteres especiales.";
        }
    }
    // Agregar event listener al campo de dirección de la empresa para validación en tiempo real
    const direccionEmpresaInput = document.querySelector("#datos-laborales input[name='domicilio_empresa']");
    direccionEmpresaInput.addEventListener("input", validarDireccionEmpresa);

    btnAnterior.addEventListener("click", function () {
        // Mostrar Datos Personales y ocultar Datos Laborales al hacer clic en "Atrás"
        datosPersonales.style.display = "block";
        btnSiguiente.style.display = "block";
        datosLaborales.style.display = "none";
        btnAnterior.style.display = "none";
        btnGuardar.style.display = "none";
    });

    const btnFinalizar = document.getElementById("btn-guardar");
    btnFinalizar.addEventListener("click", function (event) {
        const camposRequeridos = [
            "razon-social",
            "categoria-laboral",
            "rama",
            "sueldo",
            "fecha-fechaAfiliacion",
            "hora-jornada",
            "fecha-fechaIngresoTrabajo",
            "cuit-empleador",
            "direccion-empresa"
        ];
        let hayErrores = false;
        let mensajeError = "Por favor, corrija los siguientes errores antes de continuar:\n";

        camposRequeridos.forEach(function (campoId) {
            const campoError = document.getElementById(`${campoId}-error`).textContent;
            if (campoError !== "") {
                mensajeError += `- ${campoId.replace('-', ' ')}: ${campoError}\n`;
                hayErrores = true;
            }
        });

        const camposSeccionActual = document.querySelectorAll("#datos-laborales input:required");
        const camposCompletos = Array.from(camposSeccionActual).every(function (campo) {
            return campo.value.trim() !== ""; // Verificar si el campo no está vacío
        });

        if (!camposCompletos) {
            mensajeError += "- Complete todos los campos requeridos antes de continuar.\n";
            hayErrores = true;
        }

        if (hayErrores) {
            alert(mensajeError);
            event.preventDefault(); // Previene el envío del formulario si hay errores
        }
    });
});
