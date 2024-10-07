document.addEventListener('DOMContentLoaded', function() {
        // Add to Cart button functionality
        const addToCartButtons = document.querySelectorAll('[data-js="add-to-cart-button"]');
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function() {
                const url = button.getAttribute('data-url');
                const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({}) // You can add any additional data here if needed
                })
                .then(response => response.json())
                .then(data => {
                    if (data.cart_count !== undefined) {
                        console.log(`Товар добавлен в корзину. Всего товаров: ${data.cart_count}`);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });

        // Delete from Cart button functionality
        const deleteFromCartButtons = document.querySelectorAll('[data-js="delete-from-cart-button"]');
        deleteFromCartButtons.forEach(button => {
            button.addEventListener('click', function() {
                const url = button.getAttribute('data-url');
                const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Товар удалён из корзины');
                        location.reload(); // Refresh the page or update the cart view
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });

        // Change quantity buttons functionality
        const changeQuantityButtons = document.querySelectorAll('.change-quantity');
        changeQuantityButtons.forEach(button => {
            button.addEventListener('click', function() {
                const cartId = button.closest('tr').getAttribute('data-cart-id');
                const action = button.getAttribute('data-action');
                const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                const quantityElement = button.parentElement.querySelector('.quantity');
                let quantity = parseInt(quantityElement.textContent);

                if (action === 'increment') {
                    quantity += 1;
                } else if (action === 'decrement' && quantity > 1) {
                    quantity -= 1;
                }

                fetch(`/cart/update/${cartId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ quantity: quantity })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        quantityElement.textContent = quantity;
                        const totalCost = data.total_cost; // Assuming the API returns the updated total cost
                        document.getElementById('total-cost').textContent = `Итоговая стоимость: ${totalCost} ₽`;
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });