from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from webapp.models import Order

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderpart_set__part')

    orders_with_totals = []
    for order in orders:
        total_sum = sum(
            order_part.quantity * order_part.part.current_price
            for order_part in order.orderpart_set.all() if order_part.part.current_price
        )
        orders_with_totals.append({
            'order': order,
            'total_sum': total_sum
        })

    return render(request, 'profile_view.html', {
        'user': request.user,
        'orders_with_totals': orders_with_totals,
    })
