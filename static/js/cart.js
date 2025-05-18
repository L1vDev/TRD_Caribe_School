document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById('deleteModal');
    const deleteProductName = document.getElementById('deleteProductName');
    const deleteInput = document.getElementById('deleteProductId');
    let currentProductId;

    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        currentProductId = button.getAttribute('data-product-id');
        const productName = button.getAttribute('data-product-name');
        deleteInput.value = currentProductId;
        deleteProductName.textContent = productName;
    });

    const quantityModal = document.getElementById('quantityModal');
    const quantityProductName = document.getElementById('quantityProductName');
    const quantityProductPrice = document.getElementById('quantityProductPrice');
    const quantityProductImage = document.getElementById('quantityProductImage');
    const productQuantity = document.getElementById('productQuantity');
    const decreaseQuantity = document.getElementById('decreaseQuantity');
    const increaseQuantity = document.getElementById('increaseQuantity');
    const confirmQuantity = document.getElementById('confirmQuantity');
    const quantityInput = document.getElementById('quantityCartItemId');

    quantityModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        currentProductId = button.getAttribute('data-product-id');
        const productName = button.getAttribute('data-product-name');
        const productPrice = button.getAttribute('data-product-price');
        const productImage = button.getAttribute('data-product-image');

        quantityInput.value = currentProductId;
        quantityProductName.textContent = productName;
        quantityProductPrice.textContent = productPrice;
        quantityProductImage.src = productImage;
        productQuantity.value = 1;
    });

    decreaseQuantity.addEventListener('click', function () {
        if (productQuantity.value > 1) {
            productQuantity.value = parseInt(productQuantity.value) - 1;
        }
    });

    increaseQuantity.addEventListener('click', function () {
        productQuantity.value = parseInt(productQuantity.value) + 1;
    });

    const municipalitiesByProvince = JSON.parse(document.getElementById('municipalities-data').textContent);
    const provinceSelect = document.getElementById('province');
    const municipalitySelect = document.getElementById('municipality');
    const delivery_price = document.getElementById("modalShipping");
    const total_price = document.getElementById("modalTotal");
    const subtotal = parseFloat(document.getElementById("modalSubtotal").getAttribute('data-subtotal'));

    if (provinceSelect && municipalitySelect) {
        provinceSelect.addEventListener('change', function () {
            const provinceId = this.value;
            municipalitySelect.innerHTML = '<option value="" selected disabled>Selecciona un municipio</option>';
            if (municipalitiesByProvince[provinceId]) {
                municipalitiesByProvince[provinceId].forEach(function (municipality) {
                    const option = document.createElement('option');
                    option.value = municipality.id;
                    option.textContent = municipality.name;
                    option.setAttribute('data-delivery-price', municipality.price);
                    municipalitySelect.appendChild(option);
                });
                municipalitySelect.disabled = false;
            } else {
                municipalitySelect.disabled = true;
                municipalitySelect.innerHTML = '<option value="" selected disabled>Selecciona primero una provincia</option>';
            }
        });

        municipalitySelect.addEventListener('change', function () {
            const selectedOption = municipalitySelect.options[municipalitySelect.selectedIndex];
            const delivery = parseFloat(selectedOption.getAttribute('data-delivery-price')) || 0;
            delivery_price.textContent = `$${delivery.toFixed(2)}`;
            total_price.textContent = `$${(subtotal + delivery).toFixed(2)}`;
        });
    }
})