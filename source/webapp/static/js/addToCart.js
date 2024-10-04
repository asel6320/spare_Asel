async function makeRequest(url, method = "POST") {
    let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    let headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    };

    let response = await fetch(url, {
        method: method,
        headers: headers,
    });

    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(await response.text());
        console.log(error);
        throw error;
    }
}

function handleCartAction(event) {
    event.preventDefault();
    let button = event.target;
    let url = button.getAttribute('data-url');
    let action = button.getAttribute('data-action');
    let itemRow = button.closest('tr');

    if (!url) {
        console.error("URL не указан для кнопки:", button);
        return;
    }

    makeRequest(url, "POST").then(data => {
        if (action === 'add') {
            console.log("Товар добавлен в корзину:", data);
        } else if (action === 'delete') {
            console.log("Товар удален из корзины:", data);
            itemRow.remove();
        }
    }).catch(error => {
        console.error("Ошибка при обработке товара в корзине:", error);
    });
}


function onLoad() {
    let addToCartButtons = document.querySelectorAll('[data-js="add-to-cart-button"], [data-js="delete-from-cart-button"]');
    for (let button of addToCartButtons) {
        button.addEventListener('click', handleCartAction);
    }
}

window.addEventListener('load', onLoad);
