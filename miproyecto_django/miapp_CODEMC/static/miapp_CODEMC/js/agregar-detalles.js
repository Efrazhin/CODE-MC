document.getElementById('agregarDetalleBtn').addEventListener('click', function () {
    const form = document.getElementById('detalleForm');
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const detallesList = document.getElementById('detallesList');
            const li = document.createElement('li');
            li.textContent = `${data.producto_id} ${data.producto_nombre}, ${data.producto_precio}- Cantidad: ${data.cantidad}. Importe: $${data.importe}` ;
            detallesList.appendChild(li);
        } else {
            alert(data.error);
        }
    });
});