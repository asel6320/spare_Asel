from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.manager import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name_plural = "users"
        verbose_name = "user"
        db_table = "user"
