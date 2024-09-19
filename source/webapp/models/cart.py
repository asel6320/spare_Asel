from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Cart(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1, validators=(MinValueValidator(1),))
    part = models.ForeignKey('webapp.Part', related_name='carts', on_delete=models.CASCADE, verbose_name="запчасти")
    order = models.ForeignKey('webapp.Order', related_name='carts', on_delete=models.CASCADE, verbose_name="заказ", default=0)

    def __str__(self):
        return f"{self.quantity}"

    class Meta:
        db_table = 'cart'
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
