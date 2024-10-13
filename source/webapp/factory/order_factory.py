from datetime import datetime
import factory
from accounts.factory import UserFactory
from orders.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    first_name = factory.Sequence(lambda n: f'Name {n}')
    last_name = factory.Sequence(lambda n: f'Surname {n}')
    phone = factory.Faker('phone_number')
    email = factory.Faker('email')
    created_at = factory.LazyFunction(datetime.now)

    class Meta:
        model = Order
