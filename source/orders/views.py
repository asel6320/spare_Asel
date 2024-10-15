from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from carts.models import Cart
from django.conf import settings
from orders.models import Order, OrderPart
from orders.form import OrderForm
from webapp.botTG import send_notifications, send_waiting_client


class OrderCreateView(FormView):
    template_name = 'making_order.html'
    success_url = reverse_lazy('part:parts_list')
    form_class = OrderForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            user = self.request.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
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
                        delivery_address=form.cleaned_data.get('delivery_address', ''),
                    )

                    for cart_item in cart_items:
                        part = cart_item.part
                        name = part.name
                        price = part.current_price
                        quantity = cart_item.quantity

                        if part.amount < quantity:
                            raise ValidationError(
                                f'Недостаточное количество товара {name} на складе. В наличии - {part.amount}'
                            )

                        OrderPart.objects.create(
                            user=user,
                            order=order,
                            part=part,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        message = f'Новый заказ №{order.id}\nИмя: {order.first_name}\nТелефон: {order.phone}'
                        chat_id = settings.TELEGRAM_CHAT_ID
                        send_notifications(chat_id, message)
                        send_waiting_client(chat_id)
                        part.amount -= quantity
                        part.save()

                    cart_items.delete()

                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect(self.get_success_url())
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return super().form_invalid(form)
