import factory

from accounts.factory import UserFactory
from webapp.facroty import PartFactory
from webapp.models import Cart


class CartFactory(factory.django.DjangoModelFactory):
    session_key = factory.Faker("bothify", text="?" * 40)
    user = factory.SubFactory(UserFactory)
    quantity = factory.Faker("random_int", min=1, max=100)
    part = factory.SubFactory(PartFactory)

    class Meta:
        model = Cart
