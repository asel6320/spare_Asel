from django.db import models
from django.urls import reverse
from webapp.models.category import Category
from webapp.models.vehicleinfo import VehicleInfo


class Part(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="parts"
    )  # категория запчасти
    vehicle_info = models.ForeignKey(
        VehicleInfo, on_delete=models.CASCADE, related_name="parts"
    )  # информация о транспортном средстве
    name = models.CharField(max_length=255)  # название запчасти
    description = models.TextField(max_length=255)  # описание запчасти
    amount = models.PositiveIntegerField(
        verbose_name="Остаток", default=0
    )  # количество
    video_url = models.URLField(max_length=255, blank=True, null=True)
    image1 = models.ImageField(default="default.jpg", upload_to="parts/")  # изображение
    image2 = models.ImageField(
        blank=True, null=True, upload_to="parts/"
    )  # изображение 2 (опционально)
    image3 = models.ImageField(
        blank=True, null=True, upload_to="parts/"
    )  # изображение 3 (опционально)

    @property
    def current_price(self):
        return (
            self.price_history.order_by("-date_changed").first().price
            if self.price_history.exists()
            else None
        )

    @property
    def previous_price(self):
        price_history = self.price_history.order_by("-date_changed")
        if price_history.count() > 1:
            second_latest_price = price_history[1].price
            latest_price = price_history[0].price
            if second_latest_price < latest_price:
                return second_latest_price
        return None

    def get_absolute_url(self):
        return reverse("part:part_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name} for {self.vehicle_info.model.brand.name} {self.vehicle_info.model.name}"

    def to_display(self):
        return [
                self.name,
                self.vehicle_info.model.brand.name,
                self.vehicle_info.model.name,
            ]

    def get_column_headers(self):
        from django.utils.translation import gettext as _

        return [
            _('Запчасть'),
            _('Марка'),
            _('Название'),
        ]

    class Meta:
        verbose_name_plural = "Запчасти"
        verbose_name = "Запчасть"
        db_table = "car_part"
