from django.urls import path

from webapp.views import PartsListView, PartsDetailView, PartsMainView, \
    get_models, AboutUs

app_name = 'webapp'

urlpatterns = [
    path('', PartsListView.as_view(), name='parts_list'),
    path('part/<int:pk>/', PartsDetailView.as_view(), name='part_detail'),
    path('parts/', PartsMainView.as_view(), name='parts_main'),
    path('parts/about_us/', AboutUs.as_view(), name='about_us'),
    path('get-models/', get_models, name='get_models'),

]
