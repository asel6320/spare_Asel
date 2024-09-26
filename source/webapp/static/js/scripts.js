document.querySelectorAll('.carousel').forEach(function (carousel) {
    carousel.addEventListener('mouseenter', function () {
        var carouselInstance = bootstrap.Carousel.getInstance(carousel);
        carouselInstance.cycle();
    });
    carousel.addEventListener('mouseleave', function () {
        var carouselInstance = bootstrap.Carousel.getInstance(carousel);
        carouselInstance.pause();
    });
});

$(document).ready(function() {
    $('#id_brand').change(function() {
        var brand_id = $(this).val();
        if (brand_id) {
            $.ajax({
                url: '/get-models/',  // Define the URL that will return models
                data: {
                    'brand_id': brand_id
                },
                success: function(data) {
                    var model_select = $('#id_model');
                    model_select.empty();
                    $.each(data.models, function(key, value) {
                        model_select.append('<option value="' + value.id + '">' + value.name + '</option>');
                    });
                }
            });
        } else {
            $('#id_model').empty();
        }
    });
});