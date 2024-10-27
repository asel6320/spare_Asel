from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_date', 'is_active')
    list_filter = ('subscription_date', 'is_active')
    search_fields = ('email',)
