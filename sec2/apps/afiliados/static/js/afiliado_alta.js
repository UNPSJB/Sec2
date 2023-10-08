document.addEventListener("DOMContentLoaded", function () {
    const btnSiguiente = document.getElementById("btn-siguiente");
    const btnAnterior = document.getElementById("btn-anterior");
    const datosPersonales = document.getElementById("datos-personales");
    const datosLaborales = document.getElementById("datos-laborales");
    const btnGuardar = document.getElementById("btn-guardar");

    // Función para validar la fecha de nacimiento en tiempo real
    function validarFechaNacimiento() {
        const fechaNacimientoInput = document.querySelector("#datos-personales input[name='fecha_nacimiento']");
        const fechaNacimientoError = document.getElementById("fecha-nacimiento-error");
        const fechaNacimientoValue = fechaNacimientoInput.value.trim();

        // Obtener la fecha actual
        const fechaActual = new Date();
        fechaActual.setHours(0, 0, 0, 0); // Establecer hora a 00:00:00:000 para comparación

        // Convertir la fecha de nacimiento en un objeto Date
        const fechaNacimiento = new Date(fechaNacimientoValue);

        // Comprobar si la fecha de nacimiento es válida y no está en el futuro
        if (!isNaN(fechaNacimiento.getTime()) && fechaNacimiento <= fechaActual) {
            fechaNacimientoError.textContent = ""; // Fecha de nacimiento válida, elimina el mensaje de error
        } else {
            fechaNacimientoError.textContent = "Fecha no válida o en el futuro.";
        }
    }

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
            emailError.textContent = "Correo electrónico no válido.";
        }
    }

    // Agregar event listeners a los campos de fecha de nacimiento y correo electrónico para validación en tiempo real
    const fechaNacimientoInput = document.querySelector("#datos-personales input[name='fecha_nacimiento']");
    fechaNacimientoInput.addEventListener("input", validarFechaNacimiento);

    const emailInput = document.querySelector("#datos-personales input[name='mail']");
    emailInput.addEventListener("input", validarCorreoElectronico);

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

    btnAnterior.addEventListener("click", function () {
        // Mostrar Datos Personales y ocultar Datos Laborales al hacer clic en "Atrás"
        datosPersonales.style.display = "block";
        btnSiguiente.style.display = "block";
        datosLaborales.style.display = "none";
        btnAnterior.style.display = "none";
        btnGuardar.style.display = "none";
    });
});
