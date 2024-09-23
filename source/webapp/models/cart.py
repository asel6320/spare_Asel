from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name='Ключ сессии')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1, validators=(MinValueValidator(1),))
    part = models.ForeignKey('webapp.Part', related_name='carts', on_delete=models.CASCADE, verbose_name="запчасти")

    def __str__(self):
        return f"{self.quantity}"

    class Meta:
        db_table = 'cart'
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
