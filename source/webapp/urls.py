from django.urls import path

from webapp.about_us_view import get_models, AboutUs
from webapp.views.favorites import FavoriteView, FavoriteAdd, FavoriteDelete
from webapp.views import news
from webapp.views.reviews import CreateReviewView

app_name = 'webapp'

urlpatterns = [
    path('parts/about_us/', AboutUs.as_view(), name='about_us'),
    path('get-models/', get_models, name='get_models'),

    path('favorites/', FavoriteView.as_view(), name='favorites'),
    path('favorites/add/<int:pk>/', FavoriteAdd.as_view(), name='favorite_add'),
    path('favorites/<int:pk>/delete/', FavoriteDelete.as_view(), name='favorite_delete'),

    path('', news.latest_news, name='latest_news'),
    path('news/', news.news_list, name='news_list'),
    path('news/<int:news_id>/', news.news_detail, name='news_detail'),

    path('part/<int:pk>/review/create/', CreateReviewView.as_view(), name='create_review'),
]
