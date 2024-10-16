document.addEventListener('DOMContentLoaded', function() {
    // Seleccionamos todas las tarjetas de categorías
    const categoryCards = document.querySelectorAll('.category-card');

    // Hacemos clic en la categoría para mostrar/ocultar subcategorías
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            // Cerrar cualquier otra categoría activa antes de abrir la actual
            categoryCards.forEach(otherCard => {
                if (otherCard !== this) {
                    otherCard.classList.remove('active');
                }
            });

            // Alternar la clase 'active' en la categoría actual
            this.classList.toggle('active');
        });
    });

    // Seleccionamos todas las subcategorías
    const subcategoryItems = document.querySelectorAll('.subcategory-item');

    // Hacemos clic en la subcategoría para mostrar/ocultar la tabla de productos
    subcategoryItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Evitar que el evento de la categoría se dispare
            event.stopPropagation();

            // Alternar la visibilidad de la tabla de productos
            const productTable = this.querySelector('.product-table');
            if (productTable) {
                if (productTable.style.display === 'table') {
                    productTable.style.display = 'none';
                } else {
                    productTable.style.display = 'table';
                }
            }
        });
    });
});
