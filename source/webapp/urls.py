from django.urls import path
from django.views.decorators.cache import cache_page

from webapp.about_us_view import get_models, AboutUs

app_name = 'webapp'

urlpatterns = [
    path('parts/about_us/', cache_page(60*10)(AboutUs.as_view()), name='about_us'),
    path('get-models/', get_models, name='get_models'),

]
