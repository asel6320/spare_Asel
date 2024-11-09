import factory
from webapp.factory.part_factory import PartFactory

from .models import PartDocument


class PartDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartDocument

    part = factory.SubFactory(PartFactory)
    document = factory.django.FileField(
        filename="document.pdf", data=b"Some binary data"
    )
    description = factory.Faker("sentence", nb_words=100)
