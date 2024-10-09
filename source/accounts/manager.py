from django.contrib.auth.models import BaseUserManager
from random import choice


def random_phone_number():
    psw = ''
    for _ in range(10):
        psw = psw + choice(list('123456789'))

    return psw


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Поле номера телефона должна быть заполнена')
        if not username:
            raise ValueError('Поле email должен быть заполнен')
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, phone_number=None, **extra_fields):
        if not phone_number:
            phone_number = random_phone_number()
        user = self.create_user(username=username, password=password, phone_number=phone_number, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
