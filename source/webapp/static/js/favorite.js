document.addEventListener('DOMContentLoaded', function() {
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        form.addEventListener('click', function(event) {
            event.preventDefault();

            const partId = form.getAttribute('data-part-id');
            const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;
            const heartIcon = form.querySelector('.bi');

            // AJAX-запрос для добавления или удаления из избранного
            fetch(`/favorites/add/${partId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    // Меняем иконку на заполненное красное сердечко
                    heartIcon.classList.remove('bi-heart', 'text-black-50');
                    heartIcon.classList.add('bi-heart-fill', 'text-danger');
                } else if (data.status === 'removed') {
                    // Меняем иконку на белое незаполненное сердечко
                    heartIcon.classList.remove('bi-heart-fill', 'text-danger');
                    heartIcon.classList.add('bi-heart', 'text-black-50');
                }

                // Оповещение в навигационной панели
                const favoriteCountElement = document.querySelector('.nav-item .btn-light-emphasis');
                favoriteCountElement.innerHTML = `Избранное <i class="bi bi-heart-fill text-danger"></i> (<span class="favorite-count" style="color: red;">${data.favorite_count}</span>)`;

            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    });
});
