document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-detalle').forEach(button => {
        button.addEventListener('click', function() {
            const remitoId = this.getAttribute('data-id');
            const orden = this.getAttribute('data-orden')
            const fecha = this.getAttribute('data-fecha')

            document.getElementById('detalleModalLabel').innerText = `Detalles de la orden ${orden} (${fecha})`;

            fetch(`/purchases/details/${remitoId}/`)
                .then(response => response.json())
                .then(data => {
                    let contenido = '<ul class="list-group">';
                    data.detalles.forEach(detalle => {
                        contenido += `<li class="list-group-item">
                            Cód. producto: ${detalle.producto__cod_producto} <br>
                            Nombre: ${detalle.producto__nombre} <br> 
                            Tamaño: ${detalle.producto__tamaño} ${detalle.producto__unidad_medida} <br> 
                            Cantidad: ${detalle.cantidad} <br>
                            Importe: ${detalle.importe}
                        </li>`;
                    });
                    contenido += '</ul>';
                    document.getElementById('detalle-contenido').innerHTML = contenido;

                    // Mostrar el modal de Bootstrap
                    const modal = new bootstrap.Modal(document.getElementById('detalle-modal'));
                    modal.show();
                })
                .catch(error => {
                    console.error('Error al obtener los detalles:', error);
                });
        });
    });
});
