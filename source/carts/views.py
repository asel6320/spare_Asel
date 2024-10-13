from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from part.models import Part


class CartAddView(CartMixin, View):
    def post(self, request):
        part_id = request.POST.get("part_id")
        part = Part.objects.get(id=part_id)

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
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)

        cart.quantity = request.POST.get("quantity")
        cart.save()

        quantity = cart.quantity

        response_data = {
            "message": "Количество изменено",
            "quantity": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartDeleteView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)

# class CartView(View):
#
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             carts = Cart.objects.filter(user=request.user)
#         else:
#             session_key = request.session.session_key
#             if not session_key:
#                 request.session.create()
#             carts = Cart.objects.filter(session_key=request.session.session_key)
#
#         latest_price_subquery = PriceHistory.objects.filter(part=OuterRef('part')).order_by('-date_changed').values(
#             'price')[:1]
#         carts_with_price = carts.annotate(latest_price=Subquery(latest_price_subquery))
#
#         total = carts_with_price.aggregate(
#             total_sum=Sum(F('quantity') * F('latest_price'))
#         )['total_sum']
#
#         return render(request, 'cart/user_cart.html', {'carts': carts_with_price, 'total': total})
