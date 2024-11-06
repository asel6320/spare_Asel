from crm.views import (
    AdminOrderCreateView,
    AnalyticsView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomerListView,
    CustomerUpdateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
)
from django.urls import path

app_name = 'crm'

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path(
        'customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'
    ),
    path(
        'customers/<int:pk>/delete/',
        CustomerDeleteView.as_view(),
        name='customer_delete',
    ),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_edit'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/create/', AdminOrderCreateView.as_view(), name='create_order'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
