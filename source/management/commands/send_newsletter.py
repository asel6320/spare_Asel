from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from newsletter.models import Subscription


class Command(BaseCommand):
    help = "Отправка новостей подписчикам"

    def handle(self, *args, **kwargs):
        subscribers = Subscription.objects.filter(is_subscribed=True)
        subject = "Новые акции и скидки"
        message = "У нас есть отличные новости и скидки для вас!"

        for subscriber in subscribers:
            send_mail(
                subject,
                message,
                "partsauto312@gmail.com",
                [subscriber.email],
                fail_silently=False,
            )
        self.stdout.write(self.style.SUCCESS("Рассылка успешно отправлена!"))
