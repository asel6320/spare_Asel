import factory

from webapp.facroty import CarModelFactory, EngineFactory, CountryFactory
from webapp.models import VehicleInfo


class VehicleInfoFactory:
    vehicle_type = factory.Sequence(lambda n: f'Vehicle_type {n}')
    model = factory.SubFactory(CarModelFactory)
    year_of_manufacture = factory.Faker("random_int", min=1990, max=2024)
    body_type = factory.Sequence(lambda n: f'Body_type {n}')
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
