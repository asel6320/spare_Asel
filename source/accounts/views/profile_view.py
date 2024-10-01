
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    orders = request.user.orders.all()
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

    context = {
        'user': request.user,
        'orders': orders,
        'total': total,
    }
    return render(request, 'profile_view.html', context)
