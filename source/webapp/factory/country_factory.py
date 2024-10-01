import factory

from webapp.models import Country


class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Country {n}')

    class Meta:
        model = Country
