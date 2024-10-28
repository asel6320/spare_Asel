import factory
from webapp.factory.car_factory import CarModelFactory

from webapp.factory.engine_factory import EngineFactory
from webapp.factory.country_factory import CountryFactory
from webapp.models import VehicleInfo


class VehicleInfoFactory(factory.django.DjangoModelFactory):
    vehicle_type = factory.Sequence(lambda n: f"Vehicle_type {n}")
    model = factory.SubFactory(CarModelFactory)
    year_of_manufacture = factory.Faker("random_int", min=1990, max=2024)
    body_type = factory.Sequence(lambda n: f"Body_type {n}")
    engine = factory.SubFactory(EngineFactory)

    @factory.post_generation
    def countries(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.countries.add(*extracted)
        else:
            for _ in range(3):
                country = CountryFactory()
                self.countries.add(country)

    class Meta:
        model = VehicleInfo
