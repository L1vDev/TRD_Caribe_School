document.addEventListener("DOMContentLoaded", function () {
    const addToCartBtn = document.getElementById('btn-add-to-cart');
    const modalAddToCartBtn = document.getElementById('modal-add-to-cart');
    const modalQuantity = document.getElementById('modal-quantity');
    const modalBtnMinus = document.getElementById('modal-btn-minus');
    const modalBtnPlus = document.getElementById('modal-btn-plus');
    const modalSuccessMessage = document.getElementById('modal-success-message');
    const modalProductImage = document.getElementById('modal-product-image');
    const writeReviewBtn = document.getElementById('btn-write-review');
    const submitReviewBtn = document.getElementById('submit-review');
    const reviewForm = document.getElementById('review-form');
    const reviewSuccessMessage = document.getElementById('review-success-message');
    const starRating = document.getElementById('star-rating');
    const selectedRating = document.getElementById('selected-rating');

    // Inicializar los modales
    const addToCartModal = new bootstrap.Modal(document.getElementById('addToCartModal'));
    const writeReviewModal = new bootstrap.Modal(document.getElementById('writeReviewModal'));

    // Manejar la selección de estrellas
    if (starRating) {
        const stars = starRating.querySelectorAll('i');

        stars.forEach(star => {
            star.addEventListener('click', function () {
                const rating = parseInt(this.getAttribute('data-rating'));
                selectedRating.value = rating;

                // Actualizar la visualización de las estrellas
                stars.forEach(s => {
                    const starRating = parseInt(s.getAttribute('data-rating'));
                    if (starRating <= rating) {
                        s.classList.remove('bi-star');
                        s.classList.add('bi-star-fill', 'active');
                    } else {
                        s.classList.remove('bi-star-fill', 'active');
                        s.classList.add('bi-star');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function () {
                const hoverRating = parseInt(this.getAttribute('data-rating'));

                stars.forEach(s => {
                    const starRating = parseInt(s.getAttribute('data-rating'));
                    if (starRating <= hoverRating) {
                        s.classList.remove('bi-star');
                        s.classList.add('bi-star-fill');
                    } else {
                        s.classList.remove('bi-star-fill');
                        s.classList.add('bi-star');
                    }
                });
            });

            // Restaurar estrellas al quitar el mouse
            starRating.addEventListener('mouseleave', function () {
                const rating = parseInt(selectedRating.value);

                stars.forEach(s => {
                    const starRating = parseInt(s.getAttribute('data-rating'));
                    if (starRating <= rating) {
                        s.classList.remove('bi-star');
                        s.classList.add('bi-star-fill', 'active');
                    } else {
                        s.classList.remove('bi-star-fill', 'active');
                        s.classList.add('bi-star');
                    }
                });
            });
        });
    }

    // Evento para abrir el modal de escribir reseña
    writeReviewBtn.addEventListener('click', function () {
        // Resetear el formulario
        reviewForm.reset();
        reviewSuccessMessage.classList.add('d-none');

        // Resetear las estrellas
        const stars = starRating.querySelectorAll('i');
        stars.forEach(s => {
            s.classList.remove('bi-star-fill', 'active');
            s.classList.add('bi-star');
        });
        selectedRating.value = 0;

        // Mostrar el modal
        writeReviewModal.show();
    });

    // Evento para enviar la reseña
    submitReviewBtn.addEventListener('click', function (event) {
        // Validar el formulario
        const form = document.getElementById('review-form');
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            // Mostrar mensajes de validación
            form.classList.add('was-validated');
            return;
        }
    });

    // Evento para abrir el modal al hacer clic en "Añadir al Carrito"
    addToCartBtn.addEventListener('click', function () {
        // Actualizar la imagen del modal con la imagen principal seleccionada
        modalProductImage.src = document.getElementById('main-product-image').src;

        // Resetear el mensaje de éxito
        modalSuccessMessage.classList.add('d-none');

        // Mostrar el modal
        addToCartModal.show();
    });

    // Controles de cantidad en el modal
    modalBtnMinus.addEventListener('click', function () {
        let value = parseInt(modalQuantity.value);
        if (value > 1) {
            modalQuantity.value = value - 1;
        }
    });

    modalBtnPlus.addEventListener('click', function () {
        let value = parseInt(modalQuantity.value);
        modalQuantity.value = value + 1;
    });

    // Añadir al carrito desde el modal
    modalAddToCartBtn.addEventListener('click', function (event) {
        const form = document.getElementById('modal-add-to-cart-form');
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            // Mostrar mensajes de validación
            form.classList.add('was-validated');
            return;
        }
    });

    // Thumbnail slider navigation
    const slider = document.querySelector('.thumbnail-slider');
    const prevBtn = document.querySelector('.btn-light:first-child');
    const nextBtn = document.querySelector('.btn-light:last-child');
    const thumbnails = document.querySelectorAll('.product-thumbnail');

    // Scroll slider left/right
    prevBtn.addEventListener('click', function () {
        slider.scrollBy({ left: -200, behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', function () {
        slider.scrollBy({ left: 200, behavior: 'smooth' });
    });

    // Change main image when clicking thumbnails
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function () {
            // Remove active class from all thumbnails
            thumbnails.forEach(t => {
                t.classList.remove('border-primary');
            });

            // Add active class to clicked thumbnail
            this.classList.add('border-primary');

            // Update main image
            const mainImage = document.getElementById('main-product-image');
            mainImage.src = this.src;
        });
    });
})