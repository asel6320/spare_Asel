from django.shortcuts import render
from django.db.models import Count
from accounts.models import User
from orders.models import Order, OrderPart

def dashboard(request):
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='Completed').count()
    incomplete_orders = Order.objects.filter(status='Not completed').count()

    orders_by_category = OrderPart.objects.values('part__category').annotate(total=Count('id'))

    user_activity = User.objects.annotate(hour=Count('date_joined'))

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'incomplete_orders': incomplete_orders,
        'orders_by_category': orders_by_category,
        'user_activity': user_activity,
    }

    return render(request, 'dashboard.html', context)

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})