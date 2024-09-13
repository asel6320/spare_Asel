from django.urls import path

from webapp.views.parts import PartsListView, PartsDetailView, PartsByCountryView
from webapp.views.cart import CartView, CartAdd, CartDelete

app_name = 'webapp'

urlpatterns = [
    path('cart/add/<int:pk>', CartAdd.as_view(), name='part_add_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDelete.as_view(), name="cart_delete"),
    path('', PartsListView.as_view(), name='parts_list'),
    path('part/<int:pk>/', PartsDetailView.as_view(), name='part_detail'),
    path('parts/country/<int:pk>/', PartsByCountryView.as_view(), name='parts_by_country'),
]