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

function onClick(event) {
    event.preventDefault();
    let button = event.target;
    let url = button.getAttribute('data-url');

    makeRequest(url, "POST").then(data => {
        console.log("Товар добавлен в корзину:", data);
    }).catch(error => {
        console.error("Ошибка при добавлении товара в корзину:", error);
    });
}

function onLoad() {
    let addToCartButtons = document.querySelectorAll('[data-js="add-to-cart-button"]');
    for (let button of addToCartButtons) {
        button.addEventListener('click', onClick);
    }
}

window.addEventListener('load', onLoad);
