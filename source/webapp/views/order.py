from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy

from webapp.models import Cart, Order, OrderPart
from webapp.forms import OrderForm


class OrderCreateView(FormView):
    template_name = 'cart/making_order.html'
    success_url = reverse_lazy('webapp:parts_list')
    form_class = OrderForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            user = self.request.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['phone'] = user.phone_number
            initial['email'] = user.email
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        carts = Cart.objects.filter(user=user) if user else Cart.objects.filter(
            session_key=self.request.session.session_key)

        context['carts'] = carts
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user if self.request.user.is_authenticated else None
                cart_items = Cart.objects.filter(user=user) if user else Cart.objects.filter(
                    session_key=self.request.session.session_key)

                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        phone=form.cleaned_data['phone'],
                        email=form.cleaned_data['email'],
                        # delivery_address=form.cleaned_data['delivery_address'],
                    )

                    for cart_item in cart_items:
                        part = cart_item.part
                        name = part.name
                        price = part.current_price
                        quantity = cart_item.quantity

                        if part.amount < quantity:
                            raise ValidationError(
                                f'Недостаточное количество товара {name} на складе. В наличии - {part.quantity}'
                            )

                        OrderPart.objects.create(
                            order=order,
                            part=part,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        part.amount -= quantity
                        part.save()

                    cart_items.delete()

                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('webapp:order_create')

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    # def get(self, request, *args, **kwargs):
    #     form = OrderForm()
    #     if request.user.is_authenticated:
    #         user = request.user
    #         form.fields['first_name'].initial = user.first_name
    #         form.fields['last_name'].initial = user.last_name
    #         form.fields['phone'].initial = user.phone_number
    #         form.fields['email'].initial = user.email
    #     carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
    #         session_key=request.session.session_key)
    #
    #     return render(request, 'cart/cart_view.html', {
    #         'carts': carts,
    #         'order_form': form,
    #         'user': user if request.user.is_authenticated else None
    #     })
    #
    # def post(self, request, *args, **kwargs):
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         if request.user.is_authenticated:
    #             order.user = request.user
    #         order.save()
    #
    #         carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
    #             session_key=request.session.session_key)
    #         for cart in carts:
    #             OrderPart.objects.create(
    #                 order=order,
    #                 part=cart.part,
    #                 quantity=cart.quantity,
    #                 user=request.user if request.user.is_authenticated else None
    #             )
    #
    #         carts.delete()
    #         return redirect('webapp:parts_list')
    #
    #     carts = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(
    #         session_key=request.session.session_key)
    #     return render(request, 'cart/making_order.html', {'carts': carts, 'order_form': form})
