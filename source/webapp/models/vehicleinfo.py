from django.db import models
from django.utils.html import format_html

from webapp.models.car import CarModel
from webapp.models.country import Country
from webapp.models.engine import Engine

TYPE_CHOICES = [
    ('passenger', 'Легковые автомобили'),
    ('truck', 'Грузовые автомобили'),
    ('special', 'Спецтехника'),
    ('bus', 'Автобусы'),
    ('engine', 'Двигатели'),
    ('railroad', 'Ж/Д техника'),
    ('bicycle', 'Мотоциклы')
]


class VehicleInfo(models.Model):
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="vehicle_infos")
    year_of_manufacture = models.PositiveIntegerField()
    body_type = models.CharField(max_length=255, blank=True, null=True)
    countries = models.ManyToManyField(Country, related_name="vehicle_infos")
    engine = models.ForeignKey(Engine, null=True, blank=True, related_name="vehicle_infos",
                               on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} ({self.year_of_manufacture})"

    def to_display(self):
        countries_display = ', '.join(country.name for country in self.countries.all())

        return [
            self.get_vehicle_type_display(),
            self.model,
            self.year_of_manufacture,
            self.body_type if self.body_type else 'Не указано',
            countries_display if countries_display else 'Не указано',
            self.engine if self.engine else 'Не указано'
        ]

    def get_column_headers(self):
        return [
            'Тип ТС',  # vehicle_type
            'Модель',  # model
            'Год выпуска',  # year_of_manufacture
            'Тип кузова',  # body_type
            'Страны',  # countries
            'Двигатель'  # engine
        ]

    class Meta:
        verbose_name_plural = "Типы транспорта"
        verbose_name = 'Тип транспорта'
        db_table = 'vehicle'
