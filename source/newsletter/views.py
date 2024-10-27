from django.shortcuts import render, redirect
from .models import Subscription
from django.contrib import messages

def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if Subscription.objects.filter(email=email).exists():
            messages.error(request, "Этот email уже подписан.")
        else:
            Subscription.objects.create(email=email)
            messages.success(request, "Спасибо за подписку!")

        return redirect('part:parts_list')
    return render(request, 'base.html')

