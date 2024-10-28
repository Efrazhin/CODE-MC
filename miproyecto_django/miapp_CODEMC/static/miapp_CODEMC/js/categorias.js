document.addEventListener('DOMContentLoaded', function() {
    const categoryCards = document.querySelectorAll('.category-card');

    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            // Ocultar todas las listas de subcategorías
            categoryCards.forEach(c => {
                if (c !== card) {
                    c.querySelector('.subcategory-list').style.display = 'none';
                }
            });

            // Alternar la visibilidad de la subcategoría seleccionada
            const subcategoryList = card.querySelector('.subcategory-list');
            if (subcategoryList.style.display === 'block') {
                subcategoryList.style.display = 'none';
            } else {
                subcategoryList.style.display = 'block';
            }
        });
    });
});

