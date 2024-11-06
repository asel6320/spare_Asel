from django.db import models
from django.utils.html import format_html


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_display(self):
        return format_html(
            '<div style="font-weight: bold;">{}</div>',
            self.name,
        )

    class Meta:
        verbose_name_plural = "Страны"
        verbose_name = "Страна"
        db_table = "countries"
