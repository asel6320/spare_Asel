from django.urls import path

from webapp.about_us_view import get_models, AboutUs

app_name = 'webapp'

urlpatterns = [
    path('parts/about_us/', AboutUs.as_view(), name='about_us'),
    path('get-models/', get_models, name='get_models'),

]
