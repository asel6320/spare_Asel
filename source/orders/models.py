from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',
                             verbose_name='Пользователь', blank=True, null=True)
    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, null=False, blank=False, verbose_name='Телефон')
    email = models.EmailField(max_length=200, null=False, blank=False, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.first_name} {self.last_name}"

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["email", "phone", "last_name", "first_name"]

        for field in required_fields:
            if not cleaned_data.get(field):
                raise ValidationError(f"Поле {field} не может быть пустым.")

        return cleaned_data

    class Meta:
        db_table = "order"
        verbose_name = "Заказ оформления"
        verbose_name_plural = "Заказы оформления"
        ordering = ('id',)


class OrderPart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    part = models.ForeignKey('webapp.Part', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    def get_latest_price(self):
        price_history = self.part.price_history.order_by('-date_changed').first()
        return price_history.price if price_history else None

    def part_price(self):
        return round(self.part.current_price * self.quantity) if self.part.current_price else 0

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"

    class Meta:
        db_table = "order_part"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)


class OrderPartQueryset(models.QuerySet):

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
