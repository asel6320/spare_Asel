import factory
from django.utils import timezone
from webapp.models.news import News


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Sequence(lambda n: f"Новость {n}")
    short_description = factory.Faker("paragraph", nb_sentences=3, locale="ru_RU")
    full_text = factory.Faker("paragraph", nb_sentences=10, locale="ru_RU")
    image = None
    published_at = factory.LazyFunction(timezone.now)
