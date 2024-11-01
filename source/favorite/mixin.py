from favorite.models import Favorite


class FavoriteMixin:
    def get_favorite(self, request, part=None, favorite_id=None):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if part:
            query_kwargs["part"] = part
        if favorite_id:
            query_kwargs["id"] = favorite_id

        return Favorite.objects.filter(**query_kwargs).first()
