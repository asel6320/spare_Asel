from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Newsletter(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
