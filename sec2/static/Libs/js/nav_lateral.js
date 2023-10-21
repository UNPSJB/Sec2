// Obtener una referencia a los elementos de menú y botones
var menu1 = document.getElementById("menu_principal");
var menu2 = document.getElementById("menu_afiliado");
var menu3 = document.getElementById("menu_curso");  // Agrega una referencia al menú de cursos
var botonMostrarMenu1 = document.getElementById("mostrarMenuPrincipal");
var botonMostrarMenu2 = document.getElementById("mostrarMenuAfiliado");
var botonMostrarMenuCurso = document.getElementById("mostrarMenuCurso");  // Agrega una referencia al botón de "Gestión Cursos"

// Agregar eventos click a los botones para mostrar los menús correspondientes
botonMostrarMenu1.addEventListener("click", function () {
    menu1.style.display = "block"; // Mostrar el menú 1
    menu2.style.display = "none";  // Ocultar el menú 2
    menu3.style.display = "none";  // Ocultar el menú de cursos
});

botonMostrarMenu2.addEventListener("click", function () {
    menu1.style.display = "none";  // Ocultar el menú 1
    menu2.style.display = "block"; // Mostrar el menú 2
    menu3.style.display = "none";  // Ocultar el menú de cursos
});

botonMostrarMenuCurso.addEventListener("click", function () {
    menu1.style.display = "none";  // Ocultar el menú 1
    menu2.style.display = "none";  // Ocultar el menú 2
    menu3.style.display = "block"; // Mostrar el menú de cursos cuando haces clic en "Gestión Cursos"
});
