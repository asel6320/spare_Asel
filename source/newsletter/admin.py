import logging

from detail_shop import settings
from django.contrib import admin
from django.core.mail import send_mail

from .models import Newsletter, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "subscription_date", "is_active")
    list_filter = ("subscription_date", "is_active")
    search_fields = ("email",)


logger = logging.getLogger(__name__)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at")
    actions = ["send_newsletter"]

    def send_newsletter(self, request, queryset):
        subscribers = Subscription.objects.filter(is_active=True)
        emails = [subscriber.email for subscriber in subscribers]

        for newsletter in queryset:
            subject = newsletter.subject
            message = newsletter.body
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    emails,
                    fail_silently=False,
                )
                self.message_user(
                    request,
                    f"Рассылка '{subject}' отправлена {len(emails)} подписчикам.",
                )
            except Exception as e:
                logger.error(f"Ошибка при отправке рассылки: {e}")
                self.message_user(
                    request,
                    f"Ошибка при отправке рассылки '{subject}': {e}",
                    level="error",
                )

    send_newsletter.short_description = "Отправить выбранные рассылки подписчикам"
