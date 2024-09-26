import factory
from webapp.models import Engine
from webapp.models.engine import type_choices

MIN_DECIMAL = 1
MAX_DECIMAL = 100


class EngineFactory(factory.django.DjangoModelFactory):
    engine_type = factory.Iterator([e[0] for e in type_choices])
    displacement = factory.fuzzy.FuzzyDecimal(MIN_DECIMAL, MAX_DECIMAL)
    horsepower = factory.Faker("random_int", min=1, max=100)
    torque = factory.Faker("random_int", min=1, max=100)

    class Meta:
        model = Engine
