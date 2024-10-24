from django.urls import path
from django.views.decorators.cache import cache_page
from crm.views import CustomerListView

app_name = 'crm'

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers'),
]
