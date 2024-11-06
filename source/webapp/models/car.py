from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Марки машин'
        verbose_name = 'Марка машины'
        db_table = 'car_brand'


    def to_display(self):
        return [
            self.name,
        ]

    def get_column_headers(self):
        return [
            'Марка',
        ]


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="model")
    year_of_manufacture = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year_of_manufacture})"

    def to_display(self):
        return [
            self.brand.name,
            self.name,
            self.year_of_manufacture if self.year_of_manufacture else "Неуказано"
        ]

    def get_column_headers(self):
        return [
            'Марка',
            'Название',
            'Год выпуска',
        ]

    class Meta:
        verbose_name_plural = 'Модели машины'
        verbose_name = 'Модель машины'
        db_table = 'car_model'
