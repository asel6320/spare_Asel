from django.db import models

class ContactRequest(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запроса")

    def __str__(self):
        return f"{self.last_name} ({self.phone_number})"