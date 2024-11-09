import json
from datetime import timedelta

from accounts.models import User
from crm.form import AdminOrderForm, CustomerForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Sum
from django.db.models.functions.datetime import TruncDay
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from orders.models import Order, OrderPart
from part.models import Part
from crm.form import AdminOrderForm, CustomerForm
from contacts.models import ContactRequest
import json

from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView, FormView, View

class CustomerListView(ListView):
    template_name = "customer/customer_list.html"
    queryset = User.objects.all()
    context_object_name = 'customers'
    paginate_by = 10

class OrderListView(ListView):
    template_name = "order/order_list.html"
    model = Order
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects.select_related("user").prefetch_related("orderpart_set").all()
        )


class OrderDetailView(DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.object.total_price()
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = "order/order_confirm_delete.html"
    success_url = reverse_lazy("crm:orders")


class AdminOrderCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = AdminOrderForm
    template_name = "order/create_order.html"
    success_url = reverse_lazy("crm:orders")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = Part.objects.all()
        return context

    def form_valid(self, form):
        try:
            order = form.save(commit=False)
            order.user = self.request.user
            order.save()

            part_ids = form.cleaned_data["part_ids"]
            for part in part_ids:
                quantity = form.cleaned_data.get(f'quantity_{part.id}')

                if quantity > part.amount:
                    form.add_error(f'quantity_{part.id}',
                                   f"Недостаточно количества для детали: {part.name}. Доступно: {part.amount}.")
                    return self.form_invalid(form)

                OrderPart.objects.create(
                    order=order,
                    part=part,
                    quantity=quantity,
                    name=part.name,
                    price=part.current_price,
                )

            return super().form_valid(form)
        except Exception as e:
            print(f"Ошибка: {e}")
            return self.form_invalid(form)

class AnalyticsView(TemplateView):
    template_name = "analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Общая статистика заказов
        context["orders_count"] = Order.objects.count()
        context["completed_orders"] = Order.objects.filter(
            status="in_process"
        ).count()  # Adjusted for consistency
        context["pending_orders"] = Order.objects.filter(status="completed").count()
        context["delivery_orders"] = Order.objects.filter(
            requires_delivery=True
        ).count()
        context["paid_orders"] = Order.objects.filter(is_paid=True).count()

        # Расчеты заказов и дохода
        order_parts = OrderPart.objects.all()
        context["total_quantity_sold"] = (
            order_parts.aggregate(total=Count("quantity"))["total"] or 0
        )
        context["total_revenue"] = (
            order_parts.aggregate(total=Sum(F("price") * F("quantity")))["total"] or 0
        )
        context["average_order_value"] = (
            context["total_revenue"] / context["orders_count"]
            if context["orders_count"]
            else 0
        )

        # Заказы за последние 30 дней
        last_30_days = timezone.now() - timedelta(days=30)
        orders_last_30_days = (
            Order.objects.filter(created_at__gte=last_30_days)
            .annotate(day=TruncDay("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        context["orders_labels"] = json.dumps(
            [entry["day"].strftime("%Y-%m-%d") for entry in orders_last_30_days]
        )
        context["orders_data"] = json.dumps(
            [entry["count"] for entry in orders_last_30_days]
        )

        # Новые пользователи за последние 30 дней
        new_users_last_30_days = (
            User.objects.filter(date_joined__gte=last_30_days)
            .annotate(day=TruncDay("date_joined"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        context["new_users_labels"] = json.dumps(
            [entry["day"].strftime("%Y-%m-%d") for entry in new_users_last_30_days]
        )
        context["new_users_data"] = json.dumps(
            [entry["count"] for entry in new_users_last_30_days]
        )

        # Топ-5 популярных товаров
        popular_parts = (
            OrderPart.objects.values("part__name")
            .annotate(total_sold=Count("quantity"))
            .order_by("-total_sold")[:5]
        )
        context["popular_parts"] = popular_parts

        return context


class CustomerDetailView(DetailView):
    model = User
    template_name = "customer/customer_detail.html"
    context_object_name = "customer"


class CustomerUpdateView(View):
    def get(self, request, pk):
        customer = get_object_or_404(User, pk=pk)
        form = CustomerForm(instance=customer)
        return render(
            request, "customer/customer_form.html", {"form": form, "customer": customer}
        )

    def post(self, request, pk):
        customer = get_object_or_404(User, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("crm:customer_detail", pk=customer.pk)
        return render(
            request, "customer/customer_form.html", {"form": form, "customer": customer}
        )


class CustomerDeleteView(View):
    def post(self, request, pk):
        customer = get_object_or_404(User, pk=pk)
        customer.delete()
        return redirect('crm:customers')

class ContactRequestListView(ListView):
    model = ContactRequest
    template_name = 'call/contact_request_list.html'
    context_object_name = 'contact_requests'
    paginate_by = 10


