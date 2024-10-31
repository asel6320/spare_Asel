document.addEventListener('DOMContentLoaded', function () {
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        const heartIcon = form.querySelector('i');

        if (heartIcon.classList.contains('fa-solid')) {
            heartIcon.style.color = '#e81111';
        } else {
            heartIcon.style.color = '#4CAF50';
        }

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);

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
                    heartIcon.classList.remove('fa-regular', 'fa-heart');
                    heartIcon.classList.add('fa-solid', 'fa-heart');
                    heartIcon.style.color = '#e81111';
                } else if (data.status === 'removed') {
                    heartIcon.classList.remove('fa-solid', 'fa-heart');
                    heartIcon.classList.add('fa-regular', 'fa-heart');
                    heartIcon.style.color = '#4CAF50';
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
    });
});
