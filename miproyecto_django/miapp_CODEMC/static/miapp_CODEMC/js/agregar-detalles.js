

// agregar detalle
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
            li.textContent = `${data.producto_cod} ${data.producto_nombre} ${data.producto_tamaño}${data.producto_uM}, 
                ${data.producto_precio}- Cantidad: ${data.cantidad}. Importe: $${data.importe} ` ;

            const button = document.createElement('button');
            button.textContent = 'ELIMINAR';
            button.onclick = function() {
                eliminarDetalle(this, data.producto_cod);
            };

            li.appendChild(button)

            detallesList.appendChild(li);
        } else {
            alert(data.error);
        }
    });
});

const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function eliminarDetalle(button, producto_cod) {
    console.log(`Intentando eliminar el elemento con producto_cod: ${producto_cod}`);

    // Encuentra el elemento padre <li> del botón que se ha clicado
    const liElement = button.parentElement;

    fetch(`/sales/add-remmitance/del-detail/${producto_cod}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        console.log("Status:", response.status);
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error desconocido');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data);
        if (data.success) {
            // Eliminar el elemento <li> del DOM
            liElement.remove();
        } else {
            console.error("Error del servidor:", data.error);
            alert("Hubo un problema al eliminar el detalle: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Ocurrió un error al eliminar el detalle: " + error.message);
    });
}

