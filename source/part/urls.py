from django.urls import path
from part.views import PartsDetailView, PartsListView, PartsMainView

app_name = "part"

urlpatterns = [
    path("", PartsListView.as_view(), name="parts_list"),
    path(
        "part/detail/<int:pk>/",
        PartsDetailView.as_view(),
        name="part_detail",
    ),
    path("parts/", PartsMainView.as_view(), name="parts_main"),
]
