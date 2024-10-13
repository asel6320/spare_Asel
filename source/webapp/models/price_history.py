from django.db import models

from part.models import Part


class PriceHistory(models.Model):
    part = models.ForeignKey(Part, related_name='price_history', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Цена на {self.part.name} от {self.date_changed.strftime('%Y-%m-%d')}: {self.price}"

    class Meta:
        verbose_name_plural = "Истории цен"
        verbose_name = 'История цены'
        db_table = 'price_histories'
        ordering = ['-date_changed']
        app_label = 'webapp'