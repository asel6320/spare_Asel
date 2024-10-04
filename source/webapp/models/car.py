from django.db import models


# Модель марок автомобилей
class CarBrand(models.Model):
    name = models.CharField(max_length=255)  # название марки
    description = models.TextField(blank=True, null=True)  # описание

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Марки машин'
        verbose_name = 'Марка машины'
        db_table = 'car_brand'


# Модель моделей автомобилей
class CarModel(models.Model):
    name = models.CharField(max_length=255)  # название модели
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="model")  # связь с маркой
    year_of_manufacture = models.IntegerField(blank=True, null=True)  # год выпуска модели

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year_of_manufacture})"

    class Meta:
        verbose_name_plural = 'Модели машины'
        verbose_name = 'Модель машины'
        db_table = 'car_model'
