from django.contrib.auth.views import LoginView
from django.urls import path
from webapp.views import news
from webapp.views.about_us_view import AboutUs, get_models
from webapp.views.contact_offer import (
    brand_style,
    contract_offer,
    privacy_policy,
    product_docs,
    terms_of_use,
)
from webapp.views.reviews import CreateReviewView

app_name = "webapp"

urlpatterns = [
    path("parts/about_us/", AboutUs.as_view(), name="about_us"),
    path("get-models/", get_models, name="get_models"),
    path("logins/", LoginView.as_view(template_name=""), name="login"),
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
