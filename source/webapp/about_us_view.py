from django.http import JsonResponse
from django.views.generic import TemplateView

from webapp.models import CarModel


class AboutUs(TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = "О нас"
        return context


def get_models(request):
    brand_id = request.GET.get("brand_id")
    models = CarModel.objects.filter(brand_id=brand_id).values("id", "name")
    return JsonResponse({"models": list(models)})
