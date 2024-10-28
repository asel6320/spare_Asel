from django.db import models

# Модель категорий запчастей (например : легковые авто, грузовые авто и т.д.)


class Category(models.Model):
    name = models.CharField(max_length=255)  # наименование категории
    description = models.TextField(blank=True, null=True)  # описание категории

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории деталей"
        verbose_name = "Категория детали"
        db_table = "car_categories"
