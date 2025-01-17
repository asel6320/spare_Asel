from django.db import models

type_choices = [
    ("gasoline", "Бензиновый"),
    ("diesel", "Дизельный"),
    ("electric", "Электрический"),
    ("hybrid", "Гибридный"),
]


class Engine(models.Model):
    engine_type = models.CharField(max_length=50, choices=type_choices)
    displacement = models.DecimalField(max_digits=10, decimal_places=2)
    horsepower = models.PositiveIntegerField()
    torque = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_engine_type_display()} {self.displacement}L, {self.horsepower} HP"

    def to_display(self):
        return [
            self.get_engine_type_display(),
            self.displacement,
            self.horsepower,
            self.torque,
        ]

    def get_column_headers(self):
        return ['тип двигателя', 'Объем', 'Лошадиные силы', 'Крутящий момент']

    class Meta:
        verbose_name_plural = "Двигатели"
        verbose_name = "Двигатель"
        db_table = "engine"
