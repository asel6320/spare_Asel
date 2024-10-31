from accounts.models import User
from django.views.generic import ListView
from orders.models import Order


class CustomerListView(ListView):
    template_name = "customer_list.html"
    queryset = User.objects.all()
    context_object_name = "customers"


class OrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    context_object_name = "orders"
    paginate_by = 10
