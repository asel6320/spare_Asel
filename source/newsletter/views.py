from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import SubscriptionForm
from .models import Subscription


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            if Subscription.objects.filter(email=email).exists():
                messages.warning(request, "Вы уже подписаны на рассылку!")
            else:
                form.save()

                send_confirmation_email(name,email)

                messages.success(request, "Вы успешно подписались на рассылку!")
            return redirect('part:parts_list')
    else:
        form = SubscriptionForm()

    return render(request, 'subcribe.html', {'form': form})


def send_confirmation_email(name, email):
    message = f"Здравствуйте, {name}! Вы успешно подписались на нашу рассылку!"
    send_mail(
        'Подтверждение подписки',
        message,
        'partsauto312@gmail.com',
        [email],
        fail_silently=False,
    )
