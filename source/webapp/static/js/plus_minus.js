document.addEventListener('DOMContentLoaded', function () {
    let cartRows = document.querySelectorAll('tbody tr');

    cartRows.forEach(row => {
        const quantityElement = row.querySelector('.quantity');
        const cartId = row.getAttribute('data-cart-id');
        const priceElement = row.cells[2];  // The price cell
        const totalElement = row.cells[4];  // The total (Итого) cell

        row.querySelectorAll('.change-quantity').forEach(button => {
            button.addEventListener('click', function () {
                let action = this.getAttribute('data-action');
                let change = 0;

                if (action === 'increment') {
                    change = 1;
                } else if (action === 'decrement') {
                    change = -1;
                }

                updateCartQuantity(cartId, change, quantityElement, totalElement, priceElement);
            });
        });
    });

    function updateCartQuantity(cartId, change, quantityElement, totalElement, priceElement) {
        fetch(`/cart/update/${cartId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({ change: change })
        })
            .then(response => response.json())
            .then(data => {
                if (data.new_quantity !== undefined) {
                    quantityElement.textContent = data.new_quantity;

                    if (data.new_quantity === 0) {
                        row.remove();
                    }
                    let price = parseFloat(priceElement.textContent.replace('₽', '').trim());
                    let newTotal = price * data.new_quantity;
                    totalElement.textContent = `${newTotal.toFixed(2)} ₽`;

                    updateTotalCost();
                }
            });
    }

    function updateTotalCost() {
        let totalCost = 0;

        cartRows.forEach(row => {
            if (row.parentElement) {
                let quantity = parseInt(row.querySelector('.quantity').textContent);
                let price = parseFloat(row.cells[2].textContent.replace('₽', '').trim());
                totalCost += quantity * price;
            }
        });

        document.getElementById('total-cost').textContent = `Итоговая стоимость: ${totalCost.toFixed(2)} ₽`;
    }
});
