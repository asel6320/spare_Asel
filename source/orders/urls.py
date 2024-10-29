from django.urls import path
from django.views.decorators.cache import cache_page


from orders.views import OrderCreateView

app_name = "order"

urlpatterns = [
    path(
        "order/create/",
        cache_page(60 * 5)(OrderCreateView.as_view()),
        name="order_create",
    ),
]
