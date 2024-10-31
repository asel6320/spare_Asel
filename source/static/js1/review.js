function toggleReviews(partId) {
    const extraReviews = document.getElementById(`extraReviews${partId}`);
    const toggleButton = document.getElementById(`toggleReviewsBtn${partId}`);

    if (extraReviews.classList.contains('d-none')) {
        extraReviews.classList.remove('d-none');
        extraReviews.style.opacity = '1';
        toggleButton.textContent = "Скрыть отзывы";
    } else {
        extraReviews.classList.add('d-none');
        extraReviews.style.opacity = '0';
        toggleButton.textContent = "Еще отзывы";
    }
}