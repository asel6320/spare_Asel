from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель пользователя
class User(AbstractUser):
    email = models.EmailField(unique=True)  # email
    name = models.CharField(max_length=255)  # имя пользователя
    phone_number = models.CharField(max_length=20, unique=True)  # номер телефона

    def __str__(self):
        return self.name

# Модель категорий запчастей (например : легковые авто, грузовые авто и т.д.)
class Category(models.Model):
    name = models.CharField(max_length=255)  # наименование категории
    description = models.TextField(blank=True, null=True)  # описание категории

    def __str__(self):
        return self.name

# Модель марок автомобилей
class CarBrand(models.Model):
    name = models.CharField(max_length=255)  # название марки
    description = models.TextField(blank=True, null=True)  # описание

    def __str__(self):
        return self.name

# Модель моделей автомобилей
class CarModel(models.Model):
    name = models.CharField(max_length=255)  # название модели
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="models")  # связь с маркой
    year_of_manufacture = models.IntegerField(blank=True, null=True)  # год выпуска модели

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year_of_manufacture})"

# Модель для стран
class Country(models.Model):
    name = models.CharField(max_length=255)  # название страны

    def __str__(self):
        return self.name

# Модель для двигателей
class Engine(models.Model):
    type_choices = [
        ('gasoline', 'Бензиновый'),
        ('diesel', 'Дизельный'),
        ('electric', 'Электрический'),
        ('hybrid', 'Гибридный'),
    ]
    engine_type = models.CharField(max_length=50, choices=type_choices)  # тип двигателя
    displacement = models.DecimalField(max_digits=5, decimal_places=2)  # объём двигателя (литры)
    horsepower = models.PositiveIntegerField()  # мощность (лошадиные силы)
    torque = models.PositiveIntegerField()  # крутящий момент (Нм)

    def __str__(self):
        return f"{self.get_engine_type_display()} {self.displacement}L, {self.horsepower} HP"

# Модель для хранения марок, моделей и другой информации
class VehicleInfo(models.Model):
    TYPE_CHOICES = [
        ('passenger', 'Легковые автомобили'),
        ('truck', 'Грузовые автомобили'),
        ('special', 'Спецтехника'),
        ('bus', 'Автобусы'),
        ('engine', 'Двигатели'),
        ('railroad', 'Ж/Д техника'),
    ]

    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # тип транспортного средства
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="vehicle_infos")  # модель автомобиля
    year_of_manufacture = models.PositiveIntegerField()  # год выпуска
    body_type = models.CharField(max_length=255, blank=True, null=True)  # кузов
    countries = models.ManyToManyField(Country, related_name="vehicle_infos")  # страны производства
    engine = models.ForeignKey(Engine, null=True, blank=True, related_name="vehicle_infos")  # связь с двигателем

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} ({self.year_of_manufacture})"

# Модель запчастей
class Part(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="parts")  # категория запчасти
    vehicle_info = models.ForeignKey(VehicleInfo, on_delete=models.CASCADE, related_name="parts")  # информация о транспортном средстве
    name = models.CharField(max_length=255)  # название запчасти
    description = models.TextField()  # описание запчасти
    price = models.DecimalField(max_digits=10, decimal_places=2)  # цена

    def __str__(self):
        return f"{self.name} for {self.vehicle_info.model.brand.name} {self.vehicle_info.model.name}"

