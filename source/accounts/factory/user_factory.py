import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Faker

faker = Faker()

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Sequence(lambda n: f'password{n}')
    phone_number = factory.LazyAttribute(lambda _: faker.phone_number())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs['password'] = make_password(kwargs['password'])
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)

    class Meta:
        model = User
