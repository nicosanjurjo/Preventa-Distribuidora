$(document).ready(function() {

    $('#myTable').DataTable({
        order: [[0, 'desc']] });

    $('#remitos').on('click', function() {
        var url = $(this).data('url');
        $('#filtroForm').attr('action', url).submit();
    });

    $('#liquidacion').on('click', function() {
        var url = $(this).data('url');
        $('#filtroForm').attr('action', url).submit();
    });

    const anularModal = document.getElementById('anularModal');
    anularModal.addEventListener('show.bs.modal', function (event) {

        const button = event.relatedTarget;
        
        const pedidoId = button.getAttribute('data-pedido-id');
        const clienteNombre = button.getAttribute('data-cliente-nombre');
        const pedidoFecha = button.getAttribute('data-pedido-fecha');

        const modalText = anularModal.querySelector('#anularModalText');
        modalText.textContent = `¿Está seguro que desea anular el pedido #${pedidoId} del cliente ${clienteNombre} realizado el ${pedidoFecha}?`;

        const confirmarBtn = anularModal.querySelector('#confirmarAnulacionBtn');
        console.log(pedidoId);
        confirmarBtn.onclick = function() {
            $.ajax({
                url: `/gestion/anular_pedido/${pedidoId}/`,
                type: 'POST',
                success: function(data) {
                    alert(data.success);
                    window.location.reload();
                },
                error: function(xhr) {
                    const errorMessage = xhr.responseJSON.error || 'Ocurrió un error al anular el pedido.';
                    alert(`Error: ${errorMessage}`);
                }
            });
        };

    });

});
