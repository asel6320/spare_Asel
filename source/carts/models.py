from django.core.validators import MinValueValidator
from django.db import models


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.part_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name='Ключ сессии')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="Пользователь")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1, validators=(MinValueValidator(1),))
    part = models.ForeignKey('webapp.Part', related_name='carts', on_delete=models.CASCADE, verbose_name="запчасти")

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.part.name} | Количество {self.quantity}'

        return f'Анонимная корзина | Товар {self.part.name} | Количество {self.quantity}'

    def part_price(self):
        return round(self.part.current_price * self.quantity) if self.part.current_price else 0

    objects = CartQueryset().as_manager()

    class Meta:
        db_table = 'cart'
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
