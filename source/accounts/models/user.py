from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html

from accounts.manager import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=100)
    is_new = models.BooleanField(default=True, verbose_name="Новый")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def to_display(self):
        return [
            self.username,
            self.email,
            self.date_joined.strftime('%Y-%m-%d %H:%M')
        ]

    def get_column_headers(self):
        return [
            'Имя пользователя',
            'Почта',
            'Дата регестрации',
        ]

    class Meta:
        verbose_name_plural = "пользователи"
        verbose_name = 'пользователь'
        db_table = 'user'
