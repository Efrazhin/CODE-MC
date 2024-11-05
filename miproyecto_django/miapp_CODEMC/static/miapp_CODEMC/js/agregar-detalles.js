$(document).ready(function() {
    $('#add-detalle-btn').click(function() {
        var detalleForm = $('#detalle-form-container form').serialize();
        $.ajax({
            url: '{% url "agregar_detalle" %}',
            method: 'POST',
            data: detalleForm,
            success: function(response) {
                var detalleHtml = `
                    <div class="detalle" data-id="${response.id_detalle_remito}">
                        <p>Producto: ${response.producto}</p>
                        <p>Cantidad: ${response.cantidad}</p>
                        <button class="delete-detalle-btn">Eliminar</button>
                    </div>
                `;
                $('#detalles-container').append(detalleHtml);
            },
            error: function(response) {
                alert('Error al agregar detalle');
            }
        });
    });

    $(document).on('click', '.delete-detalle-btn', function() {
        var detalleId = $(this).closest('.detalle').data('id');
        $.ajax({
            url: '{% url "eliminar_detalle" id_detalle_remito=0 %}'.replace('0', detalleId),
            method: 'POST',
            success: function(response) {
                $('.detalle[data-id="' + detalleId + '"]').remove();
            },
            error: function(response) {
                alert('Error al eliminar detalle');
            }
        });
    });
});