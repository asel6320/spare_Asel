from django.urls import path
from part.views import BasePartView

from .full_change_price import UpdatePricesView
from .views import admin_home, model_add, model_delete, model_edit, model_list

app_name = "admin_panel"

urlpatterns = [
    path("", admin_home, name="admin_home"),
    path("model/<str:model_name>/", model_list, name="model_list"),
    path("model/<str:model_name>/add/", model_add, name="model_add"),
    path("model/<str:model_name>/edit/<int:pk>/", model_edit, name="model_edit"),
    path("model/<str:model_name>/delete/<int:pk>/", model_delete, name="model_delete"),
    path("update-prices/", UpdatePricesView.as_view(), name="update_prices"),
]
