from django.urls import path
from accounts.views.logout import custom_logout_view
from accounts.views.login import CustomLoginView
from accounts.views.register import register_view

from accounts.views.profile_edit import profile_edit_view
from accounts.views.profile_view import profile_view

from accounts.views.password_change_view import CustomPasswordChangeView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit_view, name='profile_edit_view'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
