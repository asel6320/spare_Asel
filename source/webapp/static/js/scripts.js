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