from django.urls import path

from webapp.views import PartsListView

app_name = 'webapp'

urlpatterns = [
    path('', PartsListView.as_view(), name='parts'),
]