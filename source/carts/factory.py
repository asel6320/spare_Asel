import factory
from accounts.factory import UserFactory
from carts.models import Cart
from django.utils import timezone
from part.factory import PartFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    session_key = factory.Faker("uuid4")
    user = factory.SubFactory(UserFactory)
    created_timestamp = factory.LazyFunction(timezone.now)
    quantity = factory.Faker("random_int", min=1, max=100)
    part = factory.SubFactory(PartFactory)
