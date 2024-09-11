from django.urls import path

from webapp.views import PartsListView, CartAdd, CartView, CartDelete

app_name = 'webapp'

urlpatterns = [
    path('', PartsListView.as_view(), name='parts'),
    path('cart/add/<int:pk>', CartAdd.as_view(), name='part_add_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDelete.as_view(), name="cart_delete"),
]