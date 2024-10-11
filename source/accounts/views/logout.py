from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


@login_required
def custom_logout_view(request):
    messages.success(request, f"{request.user.username} - Вы вышли из аккаунта")
    logout(request)
    return redirect('webapp:parts_list')
