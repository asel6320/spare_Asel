from django.db import models


# Модель для стран


class Country(models.Model):
    name = models.CharField(max_length=255)  # название страны

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Страны"
        verbose_name = "Страна"
        db_table = "countries"
