import factory
from webapp.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Category {n}')
    description = factory.Faker("paragraph", nb_sentences=10)

    class Meta:
        model = Category
