from django.urls import path
from django.views.decorators.cache import cache_page

from crm.views import CustomerListView, OrderListView, AnalyticsView, AddOrderView

app_name = 'crm'

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('orders/add/', AddOrderView.as_view(), name='add_order')
]
