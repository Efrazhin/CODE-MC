// categorias.js

// Alterna la visibilidad de los elementos hijos de un contenedor al hacer clic
function toggleDisplay(element) {
    const nextElement = element.nextElementSibling;
    if (nextElement && nextElement.style.display === 'none') {
        nextElement.style.display = 'block';
    } else if (nextElement) {
        nextElement.style.display = 'none';
    }
}
