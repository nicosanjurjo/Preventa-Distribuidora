$(document).ready(function() {

    let pedidoId = parseInt($('#pedidoid').text());

    $('#productos-table').DataTable();

    $('#all-btn').on('click', function() {
        var table = $('#productos-table').DataTable();
        table.search('').columns().search('').draw();
    });

    $('#marca-buttons').on('click', '.marca-btn', function() {
        var selectedMarca = $(this).attr('data-filter');
        var table = $('#productos-table').DataTable();
        table.column(1).search(selectedMarca).draw(); // Asume que la marca está en la segunda columna (índice 1)
    });

    // Manejar el evento de click en los botones "Agregar" en la tabla de productos
    $('#productos-table').on('click', '.add-producto', function() {
        var productoId = $(this).closest('tr').data('prodid');
        var productoMarca = $(this).closest('tr').find('td').eq(0).text();
        var productoNombre = $(this).closest('tr').find('td').eq(1).text();
        var productoPrecio = parseFloat($(this).closest('tr').find('td').eq(2).text());

        var uniqueKey = productoId + '-' + productoMarca + '-' + productoNombre;

        var productoEnPedido = $('#pedido-table tbody').find('tr[data-key="' + uniqueKey + '"]');
        if (productoEnPedido.length > 0) {
            var cantidadInput = productoEnPedido.find('.cantidad-input');
            var cantidadActual = parseInt(cantidadInput.val());
            var nuevaCantidad = cantidadActual + 1;
            cantidadInput.val(nuevaCantidad);

            var nuevoPrecioTotal = productoPrecio * nuevaCantidad;
            productoEnPedido.find('.precio-total').text(nuevoPrecioTotal);
        } else {
            var nuevoProducto = '<tr data-key="' + uniqueKey + '" data-productoid="' + productoId + '">';
            nuevoProducto += '<td>' + productoMarca + '</td>';
            nuevoProducto += '<td>' + productoNombre + '</td>';
            nuevoProducto += '<td><input type="number" class="cantidad-input" value="1" min="1"></td>';
            nuevoProducto += '<td class="precio-unitario">' + productoPrecio + '</td>';
            nuevoProducto += '<td class="precio-total" data-precio-unitario="' + productoPrecio.toFixed(2) + '">' + productoPrecio.toFixed(2) + '</td>';
            nuevoProducto += '<td><button type="button" class="btn btn-danger remove-producto">Eliminar</button></td>';
            nuevoProducto += '</tr>';

            $('#pedido-table tbody').append(nuevoProducto);
        }

        // Recalcular el total del pedido
        recalcularTotal();
    });

    $('#pedido-table').on('click', '.remove-producto', function() {
        $(this).closest('tr').remove();
        recalcularTotal();
    });

    $('#pedido-table').on('input', '.cantidad-input', function() {
        var nuevaCantidad = parseInt($(this).val());
        var productoPrecio = parseFloat($(this).closest('tr').find('.precio-total').data('precio-unitario'));

        var nuevoPrecioTotal = productoPrecio * nuevaCantidad;
        $(this).closest('tr').find('.precio-total').text(nuevoPrecioTotal);

        recalcularTotal();
    });

    function recalcularTotal() {
        var totalActualizacion = 0;
        $('#pedido-table tbody tr').each(function() {
            var precioTotal = parseFloat($(this).find('.precio-total').text());
            totalActualizacion += precioTotal;
        });
        $('#total-pedido').text(totalActualizacion);
    }

    $('#finalizar-pedido').on('click', function() {
        let actualizacionData = {
            pedido_id: pedidoId,  // Incluir el ID del pedido
            productos: [],
            total: parseInt($('#total-pedido').text())
        };

        $('#pedido-table tbody tr').each(function() {
            let productoId = $(this).data('productoid');
            let cantidad = parseInt($(this).find('.cantidad-input').val());
            let precioUnitario = parseFloat($(this).find('.precio-unitario').text());

            if (productoId) {
                actualizacionData.productos.push({
                    producto_id: productoId,
                    cantidad: cantidad,
                    precio_unitario: precioUnitario
                });
            }
        });

        enviarActualizacionAlBackend(actualizacionData);
    });

    function enviarActualizacionAlBackend(actualizacionData) {
        $.ajax({
            url: '/gestion/pedido/modificar/' + actualizacionData.pedido_id + '/',
            method: 'POST',
            data: JSON.stringify(actualizacionData),
            contentType: 'application/json',
            success: function(response) {
                alert('Pedido actualizado exitosamente');
                window.location.href='/gestion/'
            },
            error: function(xhr) {
                console.error('Error al actualizar el pedido:', xhr);
                let errorMessages = xhr.responseJSON.errors || [xhr.responseJSON.error || 'Hubo un error al actualizar el pedido'];
                alert(errorMessages.join('\n'));
            }
        });
    }
    

    // Cancelar el pedido
    $('#cancelar-pedido').click(function() {
        window.location.reload();
        // Aquí podríamos resetear el formulario o redirigir a otra página
    });

});
