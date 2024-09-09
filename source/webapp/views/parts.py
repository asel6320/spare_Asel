from django.views.generic import ListView

from webapp.models import Part


class PartsListView(ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'index.html'


