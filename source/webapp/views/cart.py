from webapp.models import Cart, Part, PriceHistory
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.db.models import Sum, F, Subquery, OuterRef

from webapp.models.order import Order


class CartAdd(View):  # добавление запчасти в корзину

    def dispatch(self, request, *args, **kwargs):
        self.part = get_object_or_404(Part, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # добавление товара в корзину с проверкой наличия на складе
        if self.part.amount > 0:
            # Здесь может быть фильтрация корзины по пользователю, если корзина привязана к юзеру
            order, created = Order.objects.get_or_create(user=request.user)
            cart, created = Cart.objects.get_or_create(part=self.part, order=order)
            if not created:
                if cart.quantity < self.part.amount:
                    cart.quantity += 1
            else:
                cart.quantity = 1
            cart.save()
        return redirect('webapp:parts_list')


class CartView(View):

    def get(self, request, *args, **kwargs):
        carts = Cart.objects.all()
        latest_price_subquery = PriceHistory.objects.filter(part=OuterRef('part')).order_by('-date_changed').values(
            'price')[:1]
        carts_with_price = carts.annotate(latest_price=Subquery(latest_price_subquery))

        total = carts_with_price.aggregate(
            total_sum=Sum(F('quantity') * F('latest_price'))
        )['total_sum']
        return render(request, 'cart/cart_view.html', {'carts': carts_with_price, 'total': total})


class CartDelete(View):

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_object_or_404(Cart, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # удаление или уменьшение количества товара в корзине
        if self.cart.quantity > 1:
            self.cart.quantity -= 1
            self.cart.save()
        elif self.cart.quantity == 1:
            self.cart.delete()
        return redirect('webapp:cart')
