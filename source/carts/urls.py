from django.urls import path

from carts.views import CartAddView, CartChangeView, CartDeleteView

app_name = "cart"

urlpatterns = [
    path("cart_add/", CartAddView.as_view(), name="cart_add"),
    path("cart_change/", CartChangeView.as_view(), name="cart_change"),
    path("cart_remove/", CartDeleteView.as_view(), name="cart_delete"),
]
