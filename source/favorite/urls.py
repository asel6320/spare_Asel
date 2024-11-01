from django.urls import path
from favorite.views import FavoriteAddView, FavoriteDelete, UserFavoriteView

app_name = "favorite"

urlpatterns = [
    path("favorites/add", FavoriteAddView.as_view(), name="favorite_add"),
    path("favorites/delete/", FavoriteDelete.as_view(), name="favorite_delete"),
    path("favorites/", UserFavoriteView.as_view(), name="favorite_template"),
]
