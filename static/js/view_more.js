document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('view-more-btn');
  if (!btn) return;
  btn.addEventListener('click', function() {
    const nextPage = btn.getAttribute('data-next-page');
    fetch(`?page=${nextPage}`, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.text())
    .then(html => {
      // Extraer solo los productos de la respuesta
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const newProducts = doc.querySelectorAll('#products-container .col');
      const container = document.getElementById('products-container');
      newProducts.forEach(col => container.appendChild(col));
      // Actualizar o quitar el botón si no hay más páginas
      const newBtn = doc.getElementById('view-more-btn');
      if (newBtn) {
        btn.setAttribute('data-next-page', newBtn.getAttribute('data-next-page'));
      } else {
        document.getElementById('view-more-row').remove();
      }
    });
  });
});