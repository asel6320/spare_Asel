from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import ContactRequestForm


def contact_request(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
