from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile_view')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль был успешно изменён.')
        return super().form_valid(form)
