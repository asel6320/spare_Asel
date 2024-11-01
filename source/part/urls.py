from django.urls import path
from django.views.decorators.cache import cache_page

from part.views import PartsListView, PartsDetailView, PartsMainView

app_name = "part"

urlpatterns = [
    path("", PartsListView.as_view(), name="parts_list"),
    path("part/<int:pk>/", PartsDetailView.as_view(), name="part_detail",),
    path("parts/", PartsMainView.as_view(), name="parts_main"),
]
