from webapp.models import Cart, Part
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.db.models import Sum, F


class CartAdd(View):  # добавление запчасти в корзину

    def dispatch(self, request, *args, **kwargs):
        self.part = get_object_or_404(Part, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # добавление товара в корзину с проверкой наличия на складе
        if self.part.amount > 0:
            # Здесь может быть фильтрация корзины по пользователю, если корзина привязана к юзеру
            cart, created = Cart.objects.get_or_create(part=self.part)
            if not created:
                if cart.quantity < self.part.amount:
                    cart.quantity += 1
            else:
                cart.quantity = 1
            cart.save()
        return redirect('webapp:parts')


class CartView(View):

    def get(self, request, *args, **kwargs):  # получение всех позиций в корзине и их общей суммы
        carts = Cart.objects.all()
        total = carts.aggregate(total_sum=Sum(F('quantity') * F('part__price')))['total_sum']
        return render(request, 'cart/cart_view.html', {'carts': carts, 'total': total})


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
