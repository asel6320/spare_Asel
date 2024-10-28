from django.contrib.auth.views import LoginView
from django.urls import path

# from django.views.decorators.cache import cache_page

from webapp.about_us_view import get_models, AboutUs
from webapp.views.favorites import FavoriteView, FavoriteAdd, FavoriteDelete
from webapp.views import news
from webapp.views.reviews import CreateReviewView

from webapp.views.contact_offer import *


app_name = "webapp"

urlpatterns = [
    path("parts/about_us/", AboutUs.as_view(), name="about_us"),
    path("get-models/", get_models, name="get_models"),
    path("logins/", LoginView.as_view(template_name=""), name="login"),
    path("favorites/", FavoriteView.as_view(), name="favorites"),
    path("favorites/add/<int:pk>/", FavoriteAdd.as_view(), name="favorite_add"),
    path(
        "favorites/<int:pk>/delete/", FavoriteDelete.as_view(), name="favorite_delete"
    ),
    path("news/", news.news_list, name="news_list"),
    path("news/<int:news_id>/", news.news_detail, name="news_detail"),
    path(
        "part/<int:pk>/review/create/", CreateReviewView.as_view(), name="create_review"
    ),
    path("contract_offer/", contract_offer, name="contract_offer"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_use/", terms_of_use, name="terms_of_use"),
    path("product_docs/", product_docs, name="product_docs"),
    path("brand_style/", brand_style, name="brand_style"),
]
