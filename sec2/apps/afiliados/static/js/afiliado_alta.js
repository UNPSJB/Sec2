document.addEventListener("DOMContentLoaded", function () {
    const btnSiguiente = document.getElementById("btn-siguiente");
    const btnAnterior = document.getElementById("btn-anterior");
    const datosPersonales = document.getElementById("datos-personales");
    const datosLaborales = document.getElementById("datos-laborales");
    const btnGuardar = document.getElementById("btn-guardar");

    btnSiguiente.addEventListener("click", function () {
        // Comprobar si todos los campos requeridos en la sección actual están llenos
        const camposSeccionActual = document.querySelectorAll("#datos-personales input:required");
        const camposCompletos = Array.from(camposSeccionActual).every(function (campo) {
            return campo.value.trim() !== ""; // Verificar si el campo no está vacío
        });

        if (camposCompletos) {
            // Ocultar Datos Personales y mostrar Datos Laborales
            datosPersonales.style.display = "none";
            btnSiguiente.style.display = "none";
            datosLaborales.style.display = "block";
            btnAnterior.style.display = "block";
            btnGuardar.style.display = "block";
        } else {
            alert("Por favor, complete todos los campos requeridos antes de continuar.");
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