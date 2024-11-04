from django.db import models
from django.utils.html import format_html


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def to_display(self):
        return format_html(
            '<div style="font-weight: bold;">{}</div>',
            self.name,
        )

    class Meta:
        verbose_name_plural = 'Категории деталей'
        verbose_name = 'Категория детали'
        db_table = 'car_categories'