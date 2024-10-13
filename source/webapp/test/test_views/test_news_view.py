import pytest
from webapp.models.news import News
from webapp.factory.news_factory import NewsFactory

@pytest.mark.django_db
def test_news_factory():

    news = NewsFactory()

    assert News.objects.count() == 1
    assert news.title.startswith('Новость')
    assert len(news.short_description) > 0
    assert len(news.full_text) > 0
    assert news.published_at is not None
