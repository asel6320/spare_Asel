from webapp.models import Cart, Part, PriceHistory
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.db.models import Sum, F, Subquery, OuterRef
from django.http import JsonResponse


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
            self.cart.delete()

        cart_count = Cart.objects.filter(
            user=request.user).count() if request.user.is_authenticated else Cart.objects.filter(
            session_key=request.session.session_key).count()

        return JsonResponse({'cart_count': cart_count})
