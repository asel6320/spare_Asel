document.addEventListener("DOMContentLoaded", function() {
    let popupDisplayed = false;
    const popupDelay = 3400;

    function showPopup() {
        if (!popupDisplayed) {
            const popup = document.getElementById('discountPopup');
            popup.style.display = 'flex';
            popupDisplayed = true;

            const closeBtn = popup.querySelector('.close-btn');
            closeBtn.addEventListener('click', () => {
                popup.style.display = 'none';
            });
        }
    }

    setTimeout(showPopup, popupDelay);
});
