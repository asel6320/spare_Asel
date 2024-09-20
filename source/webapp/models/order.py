from django.contrib.auth import get_user_model
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = "order"
        verbose_name = "Заказ оформления"
        verbose_name_plural = "Заказы оформления"
