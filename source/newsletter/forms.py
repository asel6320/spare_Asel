from django import forms
from django.core.exceptions import ValidationError
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["name", "email"]
        labels = {
            "name": "Ваше имя",
            "email": "Электронная почта",
        }
        help_texts = {
            "email": "Введите ваш адрес электронной почты для подтверждения подписки.",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and email.endswith("@example.com"):
            raise ValidationError("Регистрация с доменом example.com не разрешена.")
        return email
