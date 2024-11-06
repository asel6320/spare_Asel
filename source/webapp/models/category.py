from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def to_display(self):
        return [self.name]

    def get_column_headers(self):
        return ['Название']

    class Meta:
        verbose_name_plural = 'Категории деталей'
        verbose_name = 'Категория детали'
        db_table = 'car_categories'