from django.shortcuts import render
from django.db.models import Count
from accounts.models import User
from orders.models import Order, OrderPart

from django.views.generic import ListView
class CustomerListView(ListView):
    template_name = 'customer_list.html'
    queryset = User.objects.all()
    context_object_name = 'customers'

class OrderListView(ListView):
    template_name = 'order_list.html'
    model = Order
    context_object_name = 'orders'
    paginate_by = 10




