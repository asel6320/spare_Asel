from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель пользователя
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)  # номер телефона

    def __str__(self):
        return self.phone_number


    class Meta:
        verbose_name_plural = "users"
        verbose_name = 'user'
        db_table = 'user'