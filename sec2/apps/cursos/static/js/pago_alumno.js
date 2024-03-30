// mi_script.js
var jq = $.noConflict();
var dictadosJson;

// Función para obtener los dictados por alumno
function obtenerDictadosPorAlumno() {
    jq('#enc_alumno').change(function() {
        var rol_id = jq(this).val();
        var url = 'get_dictados_por_alumno/';

        if (rol_id && rol_id !== '0') {
            jq.ajax({
                url: '../../' + url + rol_id,
                type: 'GET',
                data: {},
                dataType: 'json',
                success: function(data) {
                    mostrarDictados(data.dictados);
                }
            });
        } else {
            limpiarContenido();
        }
    });
}

// Función para mostrar los dictados en el DOM
function mostrarDictados(dictados) {
    var datosDiv = $('#datos_titular');
    var html = '<p>Seleccione el dictado:</p>';
    
    html += '<ul>';
    dictados.forEach(function(dictado) {
        html += '<label>';
        html += '<input type="checkbox" name="dictado" value="' + dictado.pk + '" data-precio="' + dictado.precio + '" data-precio_con_descuento="' + dictado.precio_con_descuento + '" data-tipo_pago="' + dictado.tipo_pago + '" data-nombre="' + dictado.nombre + '" data-descuento="' + dictado.descuento + '">';
        html += ' ' + dictado.nombre;
        
        if (dictado.descuento > 0) {
            html += ' $' + dictado.precio_con_descuento + ' ' + dictado.tipo_pago;
            html += ' (Descuento aplicado)';
        } else {
            html += ' $' + dictado.precio + ' ' + dictado.tipo_pago;
        }
        html += '</label>';
    });
    html += '</ul>';
    datosDiv.html(html);
}

// Función para limpiar el contenido del div
function limpiarContenido() {
    $('#datos_titular').html('');
}

function obtenerDictadosSeleccionados() {
    var dictadosSeleccionados = [];

    $('input[name="dictado"]:checked').each(function () {
        dictadosSeleccionados.push({
            valor: $(this).val(),
            nombre: $(this).data('nombre'),
            precioConDescuento: $(this).data('precio_con_descuento'),
            tipo_pago: $(this).data('tipo_pago'),
            descuento: $(this).data('descuento'),
            precio: $(this).data('precio'), // Obtiene el precio desde el atributo data-precio
            cantidad: 1,
        });
    });

    return dictadosSeleccionados;
}

function calcularTotalSubtotales(dictadosSeleccionados) {
    var totalSubtotales = 0;

    for (var i = 0; i < dictadosSeleccionados.length; i++) {
        totalSubtotales += dictadosSeleccionados[i].precioConDescuento;
    }

    return totalSubtotales;
}

function generarTablaHTML(dictadosSeleccionados, totalSubtotales) {
    var tableHTML = '<table class="table table-sm table-hover">';
    tableHTML += '<thead>';
    tableHTML += '<tr>';
    tableHTML += '<th>Descripción</th>';
    tableHTML += '<th class="text-end">Precio</th>';
    tableHTML += '<th class="text-center">Desc</th>';
    tableHTML += '<th class="text-end">Precio (desc)</th>';
    tableHTML += '<th class="text-center">Cantidad</th>';
    tableHTML += '<th class="text-end">SubTotal</th>';
    tableHTML += '</tr>';
    tableHTML += '</thead>';
    tableHTML += '<tbody>';

    for (var i = 0; i < dictadosSeleccionados.length; i++) {
        tableHTML += '<tr>';
        tableHTML += '<td>' + dictadosSeleccionados[i].nombre + '</td>';
        tableHTML += '<td class="text-end">$' + dictadosSeleccionados[i].precio + '</td>';
        tableHTML += '<td class="text-center">' + dictadosSeleccionados[i].descuento + '%</td>';
        tableHTML += '<td class="text-end">$' + dictadosSeleccionados[i].precioConDescuento + '</td>';
        tableHTML += '<td class="text-center"><input type="number" class="cantidad form-control smaller-input" value="' + dictadosSeleccionados[i].cantidad + '" min="1" data-index="' + i + '"></td>';

        var precioTotal = dictadosSeleccionados[i].precioConDescuento * dictadosSeleccionados[i].cantidad;
        tableHTML += '<td class="subtotal text-end">$' + precioTotal.toFixed(2) + '</td>';
        tableHTML += '</tr>';
    }

    tableHTML += '</tbody>';
    tableHTML += '</table>';
    tableHTML += '<br><br><br>';
    tableHTML += '<p class="text-end" id="totalSubtotales">TOTAL: <strong>$' + totalSubtotales.toFixed(2) + '</strong></p>';

    return tableHTML;
}

// Función para actualizar el valor del input dictados_seleccionados
function actualizarInputDictados(dictadosSeleccionados) {
    dictadosJson = JSON.stringify(dictadosSeleccionados);
    $('#dictados_seleccionados').val(dictadosJson);
}

// Captura el cambio en los checkboxes y actualiza la sección 2
$(document).on('change', 'input[name="dictado"]', function () {
    var dictadosSeleccionados = obtenerDictadosSeleccionados();
    actualizarInputDictados(dictadosSeleccionados);

    var totalSubtotales = calcularTotalSubtotales(dictadosSeleccionados);
    var tableHTML = generarTablaHTML(dictadosSeleccionados, totalSubtotales);
    $('#seleccionados').html(tableHTML);
});

function cantidadAceptada(cantidad) {
    return cantidad >= 1 && !isNaN(cantidad);
}

function indiceValido(index) {
    return index >= 0;
}




// Captura el cambio en los campos de cantidad y actualiza los subtotales
$(document).on('change', '.cantidad', function () {
    var index = $(this).data('index'); // Obtiene el índice del elemento seleccionado
    var cantidad = parseInt($(this).val());

    if (!cantidadAceptada(cantidad)){
        cantidad = 1; // Establece la cantidad a 1
        $(this).val(cantidad); // Actualiza el valor del campo de cantidad en el HTML
    }

    var precioTotal = parseFloat($(this).closest('tr').find('td:nth-child(4)').text().replace('$', '')); // Obtiene el precio con descuento
    var subtotal = cantidad * precioTotal;
    
    $(this).closest('tr').find('.subtotal').text('$' + subtotal.toFixed(2)); // Actualiza el subtotal en la tabla

    // Verifica si el índice es válido antes de actualizar la cantidad en el arreglo seleccionados

    seleccionados = dictadosJson;
    console.log("SELECCIONADOS " + seleccionados);
    console.log("INDEX " + index);
    if (indiceValido(index)) {
        seleccionados[index].cantidad = cantidad;
        
    }

    // Recalcular el total de subtotales
    var totalSubtotales = 0;
    $('.subtotal').each(function () {
        totalSubtotales += parseFloat($(this).text().replace('$', ''));
    });
    $('#totalSubtotales').html('TOTAL : $<strong>' + totalSubtotales.toFixed(2) + '</strong>');
    $('#total_a_pagar').val(totalSubtotales.toFixed(2));
});

// Ejecutar funciones al cargar el documento
jq(document).ready(function() {
    obtenerDictadosPorAlumno();
});
