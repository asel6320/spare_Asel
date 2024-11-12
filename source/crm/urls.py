from django.urls import path
from django.views.decorators.cache import cache_page

from crm.views import (CustomerListView, OrderListView, AnalyticsView, OrderDetailView, OrderDeleteView,AdminOrderCreateView,
                       CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, ContactRequestListView, UpdateOrderStatusView, ContactRequestCreateView, DashboardView)



app_name = 'crm'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/create/', AdminOrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('contact-requests/', ContactRequestListView.as_view(), name='contact_requests'),
    path('contact-requests/create/', ContactRequestCreateView.as_view(), name='contact_request_create'),
]
