from django.urls import path
from django.views.decorators.cache import cache_page

from part.views import PartsListView, PartsDetailView, PartsMainView

app_name = 'part'

urlpatterns = [
    path('', cache_page(60*4)(PartsListView.as_view()), name='parts_list'),
    path('part/<int:pk>/', cache_page(60*3)(PartsDetailView.as_view()), name='part_detail'),
    path('parts/', cache_page(60*5)(PartsMainView.as_view()), name='parts_main'),

]
