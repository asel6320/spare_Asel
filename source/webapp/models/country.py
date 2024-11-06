from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_display(self):
        return [
            self.name,

        ]

    def get_column_headers(self):
        return ['Страна']

    class Meta:
        verbose_name_plural = "Страны"
        verbose_name = "Страна"
        db_table = "countries"
