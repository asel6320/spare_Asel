from favorite.models import Favorite


def get_favorite(request):
    if request.user.is_authenticated:
        return Favorite.objects.filter(user=request.user)

    if not request.session.session_key:
        request.session.create()
    return Favorite.objects.filter(session_key=request.session.session_key)
