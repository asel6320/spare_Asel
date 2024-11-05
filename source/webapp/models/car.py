from django.db import models
from django.utils.html import format_html


class CarBrand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Марки машин"
        verbose_name = "Марка машины"
        db_table = "car_brand"


    def to_display(self):
        return format_html(
            '<strong ">{}</strong>',
            self.name,
        )


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="model")
    year_of_manufacture = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year_of_manufacture})"

    def to_display(self):
        return format_html(
            '<div class="car-col brand" style="font-weight: bold;">{}</div>'
            '<div class="car-col model">{}</div>'
            '<div class="car-col year" style="color: gray">({})</div>',
            self.brand.name,
            self.name,
            self.year_of_manufacture if self.year_of_manufacture else "N/A"
        )

    class Meta:
        verbose_name_plural = "Модели машины"
        verbose_name = "Модель машины"
        db_table = "car_model"
