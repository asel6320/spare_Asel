from django.urls import path
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('model/<str:model_name>/', model_list, name='model_list'),
    path('model/<str:model_name>/add/', model_add, name='model_add'),
    path('model/<str:model_name>/edit/<int:pk>/', model_edit, name='model_edit'),
    path('model/<str:model_name>/delete/<int:pk>/', model_delete, name='model_delete'),
]
