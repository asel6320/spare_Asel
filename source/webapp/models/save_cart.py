from django.contrib.auth import get_user_model
from django.db import models
from webapp.models import Part

User = get_user_model()


class SaveCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_carts', verbose_name='Пользователь')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Корзина пользователя: {self.user}'

    class Meta:
        db_table = "save_cart"
        verbose_name = "Сохраненная корзина"
        verbose_name_plural = "Сохраненные корзины"


class SaveCartPart(models.Model):
    cart = models.ForeignKey(SaveCart, on_delete=models.CASCADE, related_name='cart_parts',
                             verbose_name='Сохраненная корзина')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='cart_parts', verbose_name='Деталь')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.quantity} x {self.part} в {self.cart}'

    class Meta:
        db_table = "save_cart_part"
        unique_together = ('cart', 'part')
        verbose_name = "Часть сохраненной корзины"
        verbose_name_plural = "Части сохраненной корзины"
