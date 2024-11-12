// ---------------------------------- Para mostrar detalles de un remito ----------------------------------
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-detalle').forEach(button => {
        button.addEventListener('click', function() {
            const remitoId = this.getAttribute('data-id');
            fetch(`/sales/details/${remitoId}/`)
                .then(response => response.json())
                .then(data => {
                    let contenido = '<ul>';
                    data.detalles.forEach(detalle => {
                        contenido += `<li>Producto: ${detalle.producto__nombre}, Cantidad: ${detalle.cantidad}, Importe: ${detalle.importe}</li>`;
                    });
                    contenido += '</ul>';
                    document.getElementById('detalle-contenido').innerHTML = contenido;
                    document.getElementById('detalle-modal').style.display = 'block';
                });
        });
    });

    document.getElementById('cerrar-modal').addEventListener('click', function() {
        document.getElementById('detalle-modal').style.display = 'none';
    });
});
