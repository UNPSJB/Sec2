function abrirNuevaVentana() {
    // var url = "{% url 'personas:listar_familia' afiliado.pk %}";
    var url = "{% url 'afiliados:funcionalidad_pendiente' %}";
    window.open(url, "NombreDeLaVentana", "width=800,height=600");
    // Devuelve false para evitar que el enlace se abra en la ventana actual
    return false;
}