document.addEventListener('DOMContentLoaded', function () {
    let cartRows = document.querySelectorAll('tbody tr');

    cartRows.forEach(row => {
        const quantityElement = row.querySelector('.quantity');
        const cartId = row.getAttribute('data-cart-id');

        row.querySelectorAll('.change-quantity').forEach(button => {
            button.addEventListener('click', function () {
                let action = this.getAttribute('data-action');
                let change = 0;

                if (action === 'increment') {
                    console.log("Товар добавлен в корзину:", + change);
                    change = 1;
                } else if (action === 'decrement') {
                    console.log("Товар удален из корзины:" + change);
                    change = -1;
                }
                updateCartQuantity(cartId, change, quantityElement);
            });
        });
    });

    function updateCartQuantity(cartId, change, quantityElement) {
        fetch(`/cart/update/${cartId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({change: change})
        })
            .then(response => response.json())
            .then(data => {
                if (data.new_quantity !== undefined) {
                    quantityElement.textContent = data.new_quantity;
                    updateTotalCost();
                }
            });
    }

    function updateTotalCost() {
        let totalCost = 0;

        cartRows.forEach(row => {
            let quantity = parseInt(row.querySelector('.quantity').textContent);
            let price = parseFloat(row.cells[2].textContent);
            totalCost += quantity * price;
        });

        document.getElementById('total-cost').textContent = `Итоговая стоимость: ${totalCost.toFixed(2)} ₽`;
    }
});
