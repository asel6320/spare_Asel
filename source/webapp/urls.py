from django.urls import path

from webapp.views.parts import about_us
from webapp.views import PartsListView, PartsDetailView, CartView, CartAdd, CartDelete, OrderCreateView, PartsMainView, \
    get_models, CartUpdate, CartDeleteFull, CartAddView, CartChangeView, CartRemoveView

app_name = 'webapp'

urlpatterns = [
    path('cart/add/<int:pk>', CartAdd.as_view(), name='part_add_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDelete.as_view(), name="cart_delete"),
    path('cart/<int:pk>/delete_full/', CartDeleteFull.as_view(), name="cart_delete_full"),
    path('cart/update/<int:pk>/', CartUpdate.as_view(), name='cart_update'),
    path('', PartsListView.as_view(), name='parts_list'),
    path('part/<int:pk>/', PartsDetailView.as_view(), name='part_detail'),
    path('parts/', PartsMainView.as_view(), name='parts_main'),
    path('parts/about_us/', about_us, name='about_us'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('get-models/', get_models, name='get_models'),
    path('cart_add/', CartAddView.as_view(), name='cart_add'),
    path('cart_change/', CartChangeView.as_view(), name='cart_change'),
    path('cart_remove/', CartRemoveView.as_view(), name='cart_remove'),

]
