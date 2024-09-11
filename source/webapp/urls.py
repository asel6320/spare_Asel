from django.urls import path
from webapp.views.parts import PartsListView, PartsDetailView

app_name = 'webapp'

urlpatterns = [
    path('', PartsListView.as_view(), name='parts_list'),
    path('part/<int:pk>/', PartsDetailView.as_view(), name='part_detail'),
]