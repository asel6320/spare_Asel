import factory
from accounts.factory import UserFactory
from django.contrib.auth import get_user_model
from webapp.factory.part_factory import PartFactory

from .models import Order, OrderPart

User = get_user_model()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    requires_delivery = factory.Faker("boolean")
    delivery_address = factory.Faker("address")
    payment_on_get = factory.Faker("boolean")
    is_paid = factory.Faker("boolean")
    status = factory.Faker("word")


class OrderPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderPart

    user = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
    part = factory.SubFactory(PartFactory)
    quantity = factory.Faker("random_number", digits=2)
    name = factory.Faker("word")
    price = factory.Faker("random_number", digits=5)
