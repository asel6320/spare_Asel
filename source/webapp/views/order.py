from django.shortcuts import redirect, render
from django.views import View

from webapp.models import Cart, OrderPart
from webapp.forms import OrderForm


class OrderCreate(View):

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        if request.user.is_authenticated:
            user = request.user
            form.fields['first_name'].initial = user.first_name
            form.fields['last_name'].initial = user.last_name
            form.fields['phone'].initial = user.phone_number
            form.fields['email'].initial = user.email
        carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
            session_key=request.session.session_key)

        return render(request, 'cart/cart_view.html', {
            'carts': carts,
            'order_form': form,
            'user': user if request.user.is_authenticated else None
        })

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
                session_key=request.session.session_key)
            for cart in carts:
                OrderPart.objects.create(
                    order=order,
                    part=cart.part,
                    quantity=cart.quantity,
                    user=request.user
                )

            carts.delete()
            return redirect('webapp:parts_list')

        carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
            session_key=request.session.session_key)
        return render(request, 'cart/cart_view.html', {'carts': carts, 'order_form': form})

