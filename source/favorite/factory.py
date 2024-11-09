import factory
from accounts.factory import UserFactory
from django.contrib.auth import get_user_model
from webapp.factory.part_factory import PartFactory

from .models import Favorite

User = get_user_model()


class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(UserFactory)
    session_key = factory.Faker("sha1")
    part = factory.SubFactory(PartFactory)

    @factory.post_generation
    def set_session_key_or_user(self, create, extracted, **kwargs):
        if not self.user:
            self.session_key = "random_session_key"
