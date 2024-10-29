import factory
from random import randrange
from webapp.models import CarBrand, CarModel
import datetime

CURRENT_YEAR = datetime.datetime.now().year


class CarBrandFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"CarBrand {n}")
    description = factory.Faker("paragraph", nb_sentences=10)

    class Meta:
        model = CarBrand


class CarModelFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"CarModel {n}")
    brand = factory.SubFactory(CarBrandFactory)
    year_of_manufacture = factory.LazyFunction(lambda: randrange(1990, CURRENT_YEAR))

    class Meta:
        model = CarModel
