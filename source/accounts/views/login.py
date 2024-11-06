from accounts.forms.authentication import LoginForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(
            self.request, f"{self.request.user.username} - Вы успешно вошли в аккаунт"
        )
        return redirect("part:parts_list")
