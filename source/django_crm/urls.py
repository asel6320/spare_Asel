from django.urls import path
from django.views.decorators.cache import cache_page
from django_crm.views import dashboard, user_list

app_name = 'django_crm'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', user_list, name='user_list'),
]
