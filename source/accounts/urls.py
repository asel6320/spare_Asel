from django.urls import path
from accounts.views.logout import custom_logout_view
from accounts.views.login import CustomLoginView
from accounts.views.register import register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
