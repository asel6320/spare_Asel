$(document).ready(function () {
    var successMessage = $("#jq-notification");

    // всплывающее окно через 14 секунд
    setTimeout(function () {
        $("#discountPopup").fadeIn(400);
    }, 14000);

    // Закрытие всплывающего окна
    $("#closePopup").click(function () {
        $("#discountPopup").fadeOut(400);
    });

    // Обработка отправки формы через AJAX
    $("#contactForm").on("submit", function (e) {
        e.preventDefault();

        var form = $(this);
        var formData = form.serialize();

        // клиентская валидация
        var lastName = $("#last_name").val();
        var phoneNumber = $("#phone_number").val();
        if (!lastName || !phoneNumber) {
            successMessage.html('Пожалуйста, заполните все обязательные поля.').fadeIn(400);
            setTimeout(function () {
                successMessage.fadeOut(400);
            }, 7000);
            return;
        }

        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: formData,
            success: function (data) {
                successMessage.html('Ваше сообщение отправлено!').fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                form.trigger("reset");  // Очистить форму после отправки
                $("#discountPopup").fadeOut(400);  // Закрыть всплывающее окно
            },
            error: function (data) {
                successMessage.html('Ошибка при отправке данных.').fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById('discountPopup');
    const openPopupBtn = document.getElementById('openPopup');

    if (openPopupBtn) {
        openPopupBtn.addEventListener('click', () => {
            popup.style.display = 'flex';  // Показать всплывающее окно
        });
    }

    // Закрытие всплывающего окна по кнопке закрытия
    const closeBtn = document.getElementById('closePopup');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            popup.style.display = 'none';  // Скрыть всплывающее окно
        });
    }
});
