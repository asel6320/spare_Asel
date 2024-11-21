from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from part.models import Part


class CartAddView(CartMixin, View):
    def post(self, request):
        part_id = request.POST.get("part_id")
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            return JsonResponse({"message": "Запчасть не найдена"}, status=404)

        cart = self.get_cart(request, part=part)
        if cart:

            if cart.quantity < part.amount:
                cart.quantity += 1
                cart.save()
                return JsonResponse({"message": "Количество увеличено"})
            else:
                return JsonResponse(
                    {"message": "Запчасть закончилась на складе"}, status=400
                )
        else:
            if part.amount > 0:
                Cart.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_key=(
                        request.session.session_key
                        if not request.user.is_authenticated
                        else None
                    ),
                    part=part,
                    quantity=1,
                )
                response_data = {
                    "message": "Товар добавлен в корзину",
                    "cart_items_html": self.render_cart(request),
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse(
                    {"message": "Запчасть закончилась на складе"}, status=400
                )


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        quantity = int(request.POST.get("quantity"))

        cart = self.get_cart(request, cart_id=cart_id)
        if not cart:
            return JsonResponse({"message": "Товар в корзине не найден"}, status=404)

        if quantity <= cart.part.amount:
            cart.quantity = quantity
            cart.save()
        else:
            return JsonResponse(
                {"message": "Недостаточно запчастей на складе"}, status=400
            )

        response_data = {
            "message": "Количество изменено",
            "quantity": cart.quantity,
            "cart_items_html": self.render_cart(request),
        }

        return JsonResponse(response_data)


class CartDeleteView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        if not cart:
            return JsonResponse({"message": "Товар в корзине не найден"}, status=404)

        quantity = cart.quantity
        cart.delete()
        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            "cart_items_html": self.render_cart(request),
            "stock_available": cart.part.amount,
        }

        return JsonResponse(response_data)
