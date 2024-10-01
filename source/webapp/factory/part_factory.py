import factory

from webapp.factory.category_factory import CategoryFactory
from webapp.factory.vehicleinfo_factory import VehicleInfoFactory
from webapp.models import Part


class PartFactory(factory.django.DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)
    vehicle_info = factory.SubFactory(VehicleInfoFactory)
    name = factory.Sequence(lambda n: f'Part {n}')
    description = factory.Faker("paragraph", nb_sentences=10)
    amount = factory.Faker("random_int", min=1, max=100)
    image1 = factory.django.ImageField(color='white')
    image2 = factory.django.ImageField(color='black')
    image3 = factory.django.ImageField(color='blue')

    class Meta:
        model = Part
