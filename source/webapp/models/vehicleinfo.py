from django.db import models

from webapp.models.car import CarModel, CarBrand
from webapp.models.country import Country
from webapp.models.engine import Engine


# Модель для хранения марок, моделей и другой информации
class VehicleInfo(models.Model):
    TYPE_CHOICES = [
        ('passenger', 'Легковые автомобили'),
        ('truck', 'Грузовые автомобили'),
        ('special', 'Спецтехника'),
        ('bus', 'Автобусы'),
        ('engine', 'Двигатели'),
        ('railroad', 'Ж/Д техника'),
    ]

    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # тип транспортного средства
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="vehicle_infos")  # модель автомобиля
    year_of_manufacture = models.PositiveIntegerField()  # год выпуска
    body_type = models.CharField(max_length=255, blank=True, null=True)  # кузов
    countries = models.ManyToManyField(Country, related_name="vehicle_infos")  # страны производства
    engine = models.ForeignKey(Engine, null=True, blank=True, related_name="vehicle_infos", on_delete=models.CASCADE)  # связь с двигателем

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} ({self.year_of_manufacture})"

    class Meta:
        verbose_name_plural = "vehicles"
        verbose_name = 'vehicle'
        db_table = 'vehicle'
