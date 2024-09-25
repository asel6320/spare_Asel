from django.urls import path

from webapp.views.parts import about_us
from webapp.views import PartsListView, PartsDetailView, CartView, CartAdd, CartDelete, OrderCreate, PartsMainView

app_name = 'webapp'

urlpatterns = [
    path('cart/add/<int:pk>', CartAdd.as_view(), name='part_add_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDelete.as_view(), name="cart_delete"),
    path('', PartsListView.as_view(), name='parts_list'),
    path('part/<int:pk>/', PartsDetailView.as_view(), name='part_detail'),
    path('parts/', PartsMainView.as_view(), name='parts_main'),
    #path('parts/country/<int:pk>/', PartsByCountryView.as_view(), name='parts_by_country'),
    path('parts/about_us/', about_us, name='about_us'),
    path('order/create/', OrderCreate.as_view(), name='order_create'),

]
