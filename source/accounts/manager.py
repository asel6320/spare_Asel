from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Поле номера телефона должна быть заполнена')

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, phone_number=None, **extra_fields):
        if not phone_number:
            phone_number = '0000000000'
        user = self.create_user(username, password=password, phone_number=phone_number, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
