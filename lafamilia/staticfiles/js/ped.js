$(document).ready(function() {

    $('#myTable').DataTable({
        order: [[0, 'desc']] });

    $('#remitos').on('click', function() {
        var url = $(this).data('url');  // Obtener la URL desde el atributo data-url
        $('#filtroForm').attr('action', url).submit();
    });

    // Manejar el clic en el botón "Exportar pedidos"
    $('#liquidacion').on('click', function() {
        var url = $(this).data('url');  // Obtener la URL desde el atributo data-url
        $('#filtroForm').attr('action', url).submit();
    });

    const anularModal = document.getElementById('anularModal');
    anularModal.addEventListener('show.bs.modal', function (event) {
        // Botón que disparó el modal
        const button = event.relatedTarget;
        
        // Obtener los datos del pedido desde los atributos data-
        const pedidoId = button.getAttribute('data-pedido-id');
        const clienteNombre = button.getAttribute('data-cliente-nombre');
        const pedidoFecha = button.getAttribute('data-pedido-fecha');

        // Actualizar el texto dentro del modal con los datos del pedido
        const modalText = anularModal.querySelector('#anularModalText');
        modalText.textContent = `¿Está seguro que desea anular el pedido #${pedidoId} del cliente ${clienteNombre} realizado el ${pedidoFecha}?`;

        // Actualizar el enlace del botón de confirmación
        const confirmarBtn = anularModal.querySelector('#confirmarAnulacionBtn');
        console.log(pedidoId);
        confirmarBtn.onclick = function() {
            $.ajax({
                url: `/gestion/anular_pedido/${pedidoId}/`,  // URL de la vista
                type: 'POST',
                // No enviar csrfmiddlewaretoken
                success: function(data) {
                    alert(data.success);  // Mostrar un alert en vez de un JSON
                    window.location.reload(); // Recargar la página para ver los cambios
                },
                error: function(xhr) {
                    const errorMessage = xhr.responseJSON.error || 'Ocurrió un error al anular el pedido.';
                    alert(`Error: ${errorMessage}`);  // Muestra el error en un alert
                }
            });
        };

    });

});
