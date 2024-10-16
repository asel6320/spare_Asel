document.addEventListener('DOMContentLoaded', function () {
    const favoriteForms = document.querySelectorAll('.favorite-form'); // Выбираем все формы с классом "favorite-form"
    favoriteForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            const partId = form.getAttribute('data-part-id');
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    form.querySelector('i').classList.remove('bi-heart');
                    form.querySelector('i').classList.add('bi-heart-fill', 'text-danger');
                } else if (data.status === 'removed') {
                    form.querySelector('i').classList.remove('bi-heart-fill', 'text-danger');
                    form.querySelector('i').classList.add('bi-heart', 'text-black-50');
                }
                const favoriteCountElement = document.querySelector('.favorites-count');
                if (favoriteCountElement) {
                    favoriteCountElement.textContent = data.favorite_count;
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
        const isFavorite = form.querySelector('i').classList.contains('bi-heart-fill');
        if (isFavorite) {
            form.querySelector('i').classList.add('bi-heart-fill', 'text-danger');
        }
    });
});