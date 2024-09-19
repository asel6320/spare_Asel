from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from accounts.forms.auth_form import LoginForm
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('webapp:parts_list')