from datetime import date

from orders.models import Order
from contacts.models import ContactRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def notification_counts(request):
    return {
        'new_users_count': min(User.objects.filter(is_new=True).count(), 10),
        'new_orders_count': min(Order.objects.filter(is_new=True).count(), 10),
        'new_contacts_count': min(ContactRequest.objects.filter(is_new=True).count(), 10),
        'total_orders_count': Order.objects.count(),
        'active_orders_count': Order.objects.filter(status='in_process').count(),
        'todays_orders_count': Order.objects.filter(
            created_at__date=date.today()
        ).count(),
    }