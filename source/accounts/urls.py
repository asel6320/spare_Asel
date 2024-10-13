from django.urls import path
from accounts.views.logout import custom_logout_view
from accounts.views.login import CustomLoginView
from accounts.views.register import UserRegistrationView
from accounts.views.profile import UserProfileView
from accounts.views.profile import UserCartView
from accounts.views.password_change_view import CustomPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('user/cart', UserCartView.as_view(), name='cart'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
