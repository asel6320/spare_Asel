$(document).ready(function () {
    var successMessage = $("#jq-notification");

    $(document).off("click", ".add-to-favorite").on("click", ".add-to-favorite", function (e) {
        e.preventDefault();

        var part_id = $(this).data("part-id");
        var add_to_favorite_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_favorite_url,
            data: {
                part_id: part_id,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            cache: false,
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 2000);
            },
            error: function () {
                console.log("Ошибка при добавлении товара в избранное");
            },
        });
    });

    $(document).on("click", ".favorite-delete", function (e) {
        e.preventDefault();

        var favorite_id = $(this).data("favorite-id");
        var remove_from_favorite_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_favorite_url,
            data: {
                favorite_id: favorite_id,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            cache: false,
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 2000);

                $(`.row>div[data-card="${favorite_id}"]`).remove();
            },
            error: function () {
                console.log("Ошибка при удалении товара из избранного");
            },
        });
    });
});
