import json

from webapp.models import Cart, Part, PriceHistory
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.db.models import Sum, F, Subquery, OuterRef
from django.http import JsonResponse

from webapp.views.mixins import CartMixin


class CartAdd(View):

    def dispatch(self, request, *args, **kwargs):
        self.part = get_object_or_404(Part, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.part.amount > 0:
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(part=self.part, user=request.user)
            else:
                session_key = request.session.session_key or request.session.create()
                cart, created = Cart.objects.get_or_create(part=self.part, session_key=session_key)
            if created:
                cart.quantity = 1
            elif cart.quantity < self.part.amount:
                cart.quantity += 1

            cart.save()

        cart_count = Cart.objects.filter(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None
        ).count()

        return JsonResponse({'cart_count': cart_count})


class CartView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            carts = Cart.objects.filter(session_key=request.session.session_key)

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

    def post(self, request, *args, **kwargs):
        if self.cart.quantity > 1:
            self.cart.quantity -= 1
            self.cart.save()
        elif self.cart.quantity == 1:
            self.cart.quantity = 1

        cart_count = Cart.objects.filter(
            user=request.user).count() if request.user.is_authenticated else Cart.objects.filter(
            session_key=request.session.session_key).count()

        return JsonResponse({'cart_count': cart_count})


class CartUpdate(View):
    def dispatch(self, request, *args, **kwargs):
        self.cart = get_object_or_404(Cart, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        change = data.get('change', 0)

        if change == -1 and self.cart.quantity > 1:
            self.cart.quantity -= 1
        elif change == 1 and self.cart.quantity < self.cart.part.amount:
            self.cart.quantity += 1

        self.cart.save()

        return JsonResponse({'new_quantity': self.cart.quantity})


class CartDeleteFull(View):
    def dispatch(self, request, *args, **kwargs):
        self.cart = get_object_or_404(Cart, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.cart.delete()
        total_cost = self.calculate_total_cost(request.user)
        return JsonResponse({'success': True, 'total_cost': total_cost})

    def calculate_total_cost(self, user):

        total = 0
        if user.is_authenticated:
            carts = Cart.objects.filter(user=user)
        else:
            carts = Cart.objects.filter(session_key=self.request.session.session_key)

        for cart in carts:
            total += cart.quantity * cart.part.current_price

        return total


class CartAddView(CartMixin, View):
    def post(self, request):
        part_pk = request.POST.get("part_pk")
        part = Part.objects.get(part_pk=part_pk)

        cart = self.get_cart(request, part=part)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                part=part, quantity=1)

        response_data = {
            "message": "Товар добавлен в корзину",
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_pk = request.POST.get("cart_pk")

        cart = self.get_cart(request, cart_pk=cart_pk)

        cart.quantity = request.POST.get("quantity")
        cart.save()

        quantity = cart.quantity

        response_data = {
            "message": "Количество изменено",
            "quantity": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_pk = request.POST.get("cart_pk")

        cart = self.get_cart(request, cart_pk=cart_pk)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
