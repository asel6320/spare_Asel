from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html

from accounts.manager import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def to_display(self):
        return format_html(
            '<span class="user-col username"><strong>{}</strong></span>'
            '<span class="user-col email" style="color: green; font-weight: bold;">{}</span>'
            '<span class="user-col date" style="color: gray;">{}</span>',
            self.username,
            self.email,
            self.date_joined.strftime('%Y-%m-%d %H:%M')
        )

    class Meta:
        verbose_name_plural = "пользователи"
        verbose_name = 'пользователь'
        db_table = 'user'
