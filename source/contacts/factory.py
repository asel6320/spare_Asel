import factory
from contacts.models import ContactRequest


class ContactRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactRequest

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    comments = factory.Faker("text", max_nb_chars=200)
    created_at = factory.Faker("date_time_this_year")
