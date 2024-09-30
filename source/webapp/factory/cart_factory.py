import factory

from accounts.factory import UserFactory
from webapp.factory.part_factory import PartFactory
from webapp.models import Cart


class CartFactory(factory.django.DjangoModelFactory):
    session_key = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=70),
        yes_declaration=factory.Faker("bothify", text="?" * 40),
        no_declaration=None
    )
    user = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=70),
        yes_declaration=factory.SubFactory(UserFactory),
        no_declaration=None
    )
    quantity = factory.Faker("random_int", min=1, max=100)
    part = factory.SubFactory(PartFactory)

    class Meta:
        model = Cart
