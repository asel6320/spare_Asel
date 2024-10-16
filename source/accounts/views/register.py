from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib import auth, messages
from accounts.forms.registration import RegisterForm
from carts.models import Cart


class UserRegistrationView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('part:parts_list')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context
