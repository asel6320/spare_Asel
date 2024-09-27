import factory
from random import randrange
from webapp.models import CarBrand, CarModel

MIN_PRICE = 1
MAX_PRICE = 100


class CarBrandFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'CarBrand {n}')
    description = factory.Faker("paragraph", nb_sentences=10)

    class Meta:
        model = CarBrand


class CarModelFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'CarModel {n}')
    brand = factory.SubFactory(CarBrandFactory)
    year_of_manufacture = factory.LazyAttribute(randrange(MIN_PRICE, MAX_PRICE))

    class Meta:
        model = CarModel
