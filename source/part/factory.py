import factory
from factory.django import DjangoModelFactory
from part.models import Part
from webapp.factory.category_factory import CategoryFactory
from webapp.factory.vehicleinfo_factory import VehicleInfoFactory


class PartFactory(DjangoModelFactory):
    class Meta:
        model = Part

    category = factory.SubFactory(CategoryFactory)
    vehicle_info = factory.SubFactory(VehicleInfoFactory)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    amount = factory.Faker("random_int", min=0, max=100)
    video_url = factory.Faker("url")
    image1 = factory.django.ImageField(filename="default_part_image.jpg")
    image2 = factory.django.ImageField(filename="default_part_image.jpg")
    image3 = factory.django.ImageField(filename="default_part_image.jpg")

    @factory.post_generation
    def price_history(self, create, extracted, **kwargs):
        if create:
            from webapp.models import PriceHistory

            PriceHistory.objects.create(part=self, price=100.0)
            PriceHistory.objects.create(part=self, price=110.0)
