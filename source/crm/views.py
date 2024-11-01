from datetime import timedelta
from django.utils import timezone
from django.urls import reverse_lazy

from django.db.models.functions.datetime import TruncDay
from django.shortcuts import render
from django.db.models import Count, Sum, F, Avg
from accounts.models import User
from orders.models import Order, OrderPart
from crm.form import OrderForm

from django.views.generic import ListView, TemplateView, CreateView


class CustomerListView(ListView):
    template_name = 'customer_list.html'
    queryset = User.objects.all()
    context_object_name = 'customers'

class OrderListView(ListView):
    template_name = 'order_list.html'
    model = Order
    context_object_name = 'orders'
    paginate_by = 10


class AnalyticsView(TemplateView):
    template_name = 'analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Общая статистика заказов
        context['orders_count'] = Order.objects.count()
        context['completed_orders'] = Order.objects.filter(status="Completed").count()
        context['pending_orders'] = Order.objects.filter(status="Pending").count()
        context['delivery_orders'] = Order.objects.filter(requires_delivery=True).count()
        context['paid_orders'] = Order.objects.filter(is_paid=True).count()

        # Расчеты заказов и дохода
        order_parts = OrderPart.objects.all()
        context['total_quantity_sold'] = order_parts.aggregate(total=Count('quantity'))['total'] or 0
        context['total_revenue'] = order_parts.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0
        context['average_order_value'] = context['total_revenue'] / context['orders_count'] if context[
            'orders_count'] else 0

        # Заказы за последние 30 дней
        last_30_days = timezone.now() - timedelta(days=30)
        orders_last_30_days = (
            Order.objects.filter(created_at__gte=last_30_days)
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        context['orders_labels'] = [entry['day'].strftime('%Y-%m-%d') for entry in orders_last_30_days]
        context['orders_data'] = [entry['count'] for entry in orders_last_30_days]

        # Новые пользователи за последние 30 дней
        new_users_last_30_days = (
            User.objects.filter(date_joined__gte=last_30_days)
            .annotate(day=TruncDay('date_joined'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        context['new_users_labels'] = [entry['day'].strftime('%Y-%m-%d') for entry in new_users_last_30_days]
        context['new_users_data'] = [entry['count'] for entry in new_users_last_30_days]

        # Топ-5 популярных товаров
        popular_parts = (
            OrderPart.objects.values('part__name')
            .annotate(total_sold=Count('quantity'))
            .order_by('-total_sold')[:5]
        )
        context['popular_parts'] = popular_parts

        return context


class AddOrderView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'add_order.html'
    success_url = reverse_lazy('crm:orders')

    def form_valid(self, form):
        # Assign the logged-in user to the order
        form.instance.user = self.request.user  # This line assigns the user
        return super().form_valid(form)


