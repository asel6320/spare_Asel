from django.db.models import Subquery, OuterRef
from webapp.models.favorites import Favorite
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from part.models import Part
from webapp.models.price_history import PriceHistory
class FavoriteAdd(View):
    def dispatch(self, request, *args, **kwargs):
        self.part = get_object_or_404(Part, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if self.part.amount > 0:
            if request.user.is_authenticated:
                favorite, created = Favorite.objects.get_or_create(part=self.part, user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    session_key = request.session.create()
                favorite, created = Favorite.objects.get_or_create(part=self.part, session_key=session_key)
            if not created:
                favorite.delete()
                status = 'removed'
            else:
                status = 'added'
            favorite_count = Favorite.objects.filter(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None
            ).count()
            return JsonResponse({
                'status': status,
                'favorite_count': favorite_count
            })
        return JsonResponse({'status': 'error', 'message': 'Запчасть отсутствует на складе'}, status=400)
class FavoriteView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create()
            favorites = Favorite.objects.filter(session_key=session_key)
        latest_price_subquery = PriceHistory.objects.filter(part=OuterRef('part')).order_by('-date_changed').values('price')[:1]
        favorites_with_price = favorites.annotate(latest_price=Subquery(latest_price_subquery))
        if not favorites_with_price.exists():
            return render(request, 'favorites/favorites.html', {'favorites': favorites_with_price, 'message': 'Нет избранных товаров.'})
        return render(request, 'favorites/favorites.html', {'favorites': favorites_with_price})
class FavoriteDelete(View):
    def dispatch(self, request, *args, **kwargs):
        self.favorite = get_object_or_404(Favorite, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.favorite.delete()
        return redirect('webapp:favorites')