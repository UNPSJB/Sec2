document.addEventListener('DOMContentLoaded', function () {
    // Agregar funcionalidad para mostrar/ocultar los submenús con un clic
    const submenuButtons = document.querySelectorAll('.submenu-toggle')

    submenuButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const submenu = button.nextElementSibling
            submenu.classList.toggle('show');
        })
    })
});