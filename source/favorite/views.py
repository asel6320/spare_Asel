from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from favorite.mixin import FavoriteMixin
from favorite.models import Favorite
from favorite.utils import get_favorite
from part.models import Part


class FavoriteAddView(FavoriteMixin, View):

    def post(self, request):
        part_id = request.POST.get("part_id")
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Товар не найден"}, status=404
            )

        if request.user.is_authenticated:
            favorite_item, created = Favorite.objects.get_or_create(
                user=request.user, part=part
            )
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            favorite_item, created = Favorite.objects.get_or_create(
                session_key=session_key, part=part
            )

        if created:
            status = "added"
            message = "Товар добавлен в избранное"
        else:
            status = "removed"
            favorite_item.delete()
            message = "Товар удалён из избранного"

        response_data = {
            "status": status,
            "message": message,
        }
        return JsonResponse(response_data)


class FavoriteDelete(FavoriteMixin, View):
    def post(self, request, *args, **kwargs):
        favorite_id = request.POST.get("favorite_id")
        favorite = self.get_favorite(request, favorite_id=favorite_id)
        if favorite:
            favorite.delete()

        response_data = {
            "message": "Товар удален из избранных",
        }
        return JsonResponse(response_data)


class UserFavoriteView(TemplateView):
    template_name = "favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = get_favorite(self.request)
        return context
