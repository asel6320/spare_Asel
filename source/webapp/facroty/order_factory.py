from datetime import datetime

import factory

from accounts.factory import UserFactory
from webapp.models import Order

MIN_DECIMAL = 1
MAX_DECIMAL = 100


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    first_name = factory.Sequence(lambda n: f'Name {n}')
    last_name = factory.Sequence(lambda n: f'Surname {n}')
    phone = factory.Faker('phone_number')
    email = factory.LazyAttribute(lambda o: f'n@gmail.com {o.first_name}')
    created_at = factory.LazyFunction(datetime.now)

    class Meta:
        model = Order
