from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch

from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages

from accounts.forms.profile import ProfileForm
from webapp.models import Order, OrderPart


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderpart_set",
                queryset=OrderPart.objects.select_related("product"),
            )
        ).order_by("-id")

        total = 0

        for order in orders:
            order_total = 0
            for order_part in order.orderpart_set.all():
                latest_price = order_part.get_latest_price()
                order_part.latest_price = latest_price
                if latest_price:
                    line_total = latest_price * order_part.quantity
                    order_total += line_total
                    total += line_total
                else:
                    order_part.latest_price = None

            order.total = order_total

        context['orders'] = orders
        context['total'] = total
        return context

