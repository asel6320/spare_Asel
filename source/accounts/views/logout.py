from django.shortcuts import redirect
from django.contrib.auth import logout


def custom_logout_view(request):
    logout(request)
    return redirect('webapp:parts_list')
