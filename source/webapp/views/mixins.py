from django.template.loader import render_to_string
from django.urls import reverse
from webapp.models import Cart
from webapp.views.utils import get_user_carts


class CartMixin:
    def get_cart(self, request, part=None, cart_pk=None):

        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if part:
            query_kwargs["part"] = part
        if cart_pk:
            query_kwargs["pk"] = cart_pk

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        referer = request.META.get('HTTP_REFERER')
        if reverse('webapp:order_create') in referer:
            context["order"] = True

        return render_to_string(
            "cart/included_cart.html", context, request=request
        )
