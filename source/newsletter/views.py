import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages
from django.shortcuts import render
from .forms import SubscriptionForm
from .models import Subscription
from django.conf import settings

logger = logging.getLogger(__name__)

def subscribe(request):
    form = SubscriptionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        name = form.cleaned_data["name"]

        subscription, created = Subscription.objects.get_or_create(
            email=email, defaults={'name': name, 'is_active': True}
        )

        if not created:
            if subscription.is_active:
                subscription.email=email
                messages.success(request, "Вы уже подписаны на рассылку!")
            else:
                subscription.is_active = True
                subscription.name = name
                subscription.save()
                messages.success(request, "Ваша подписка была повторно активирована.")
        else:
            if send_confirmation_email(name, email):
                messages.success(request, "Вы успешно подписались на рассылку!")
            else:
                messages.error(request, "Произошла ошибка при отправке письма подтверждения.")

    return render(request, "index.html")


def send_confirmation_email(name, email):
    subject = "Подтверждение подписки"
    message_body = (
        f"Здравствуйте, {name}!\n\n"
        "Вы успешно подписались на нашу рассылку!\n\n"
        "Контакты:\n"
        "info@abc-auto.com\n"
        "+996 (555) 003 539\n"
        "Бишкек, Малдыбаева 7/1"
    )
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        logger.info("Connecting to SMTP server...")
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30) as server:
            logger.info("Starting TLS encryption...")
            server.starttls()
            logger.info("Logging in to SMTP server...")
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            logger.info(f"Sending email to {email}...")
            server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            logger.info("Email sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке письма подтверждения для {email}: {e}")
        return False